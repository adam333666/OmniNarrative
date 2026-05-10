from __future__ import annotations

import os
from datetime import UTC, datetime, timedelta
from pathlib import Path

TEST_DB_PATH = Path("/tmp/multi_media_m31_regression.db")
os.environ.setdefault("DATABASE_URL", f"sqlite+pysqlite:///{TEST_DB_PATH}")
os.environ.setdefault("INTERNAL_API_KEY", "change-me")

import pytest

from app.api.routes.creations import (
    export_generation_json,
    export_generation_markdown,
    export_video_payload,
    generate_creation,
    get_generation_result,
    get_generation_status,
)
from app.core.config import settings
from app.schemas.creation_request import CreationRequest
from app.db.bootstrap import bootstrap_database
from app.db.repositories.generation_job_event_repository import SqlAlchemyGenerationJobEventRepository
from app.db.repositories.generation_job_repository import SqlAlchemyGenerationJobRepository
from app.db.repositories.generation_result_repository import SqlAlchemyGenerationResultRepository
from app.db.session import get_engine, get_session_factory
from app.schemas.trend_template import PlatformTrendTemplate
from app.services.generation_pipeline.coordinator import generation_materialization_coordinator
from app.services.generation_pipeline.runner import generation_execution_runner
from app.services.generation_pipeline.result_builder import generation_result_builder
from app.services.generation_pipeline.store import GenerationPipelineStore, generation_pipeline_store
from app.services.trend_strategy.repository import TrendTemplateRepository
from app.services.trend_strategy.service import trend_strategy_service
from tests.test_m46_export_payload_compat import build_result as build_export_ready_result

VALID_PAYLOAD = {
    "theme_text": "我想做一个关于时间旅行悖论的内容",
    "content_type": "science_popularization",
    "target_platform": "bilibili",
    "target_audience_text": "18到28岁，喜欢科幻设定和逻辑推理的观众",
    "style_tone": "suspense",
    "custom_style_text": "保持一点烧脑感",
}


def reset_database() -> None:
    get_engine().dispose()
    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink()
    get_engine.cache_clear()
    get_session_factory.cache_clear()
    generation_execution_runner.shutdown(wait=False)
    bootstrap_database()
    generation_pipeline_store.repository = SqlAlchemyGenerationJobRepository()
    generation_pipeline_store.result_repository = SqlAlchemyGenerationResultRepository()
    generation_pipeline_store.event_repository = SqlAlchemyGenerationJobEventRepository()
    trend_strategy_service.repository = TrendTemplateRepository()
    generation_result_builder.result_repository = SqlAlchemyGenerationResultRepository()
    generation_materialization_coordinator.result_repository = SqlAlchemyGenerationResultRepository()
    settings.internal_api_key = "change-me"
    settings.generation_auto_start_enabled = False


def mark_generation_done(generation_id: str) -> None:
    GenerationPipelineStore(
        repository=SqlAlchemyGenerationJobRepository(),
        result_repository=SqlAlchemyGenerationResultRepository(),
    ).mark_ready_for_result(generation_id)


def build_stub_result(generation_id: str):
    result = build_export_ready_result()
    return result.model_copy(
        update={
            "export_meta": {
                **result.export_meta,
                "generation_id": generation_id,
            }
        }
    )


def create_generation() -> str:
    created = generation_pipeline_store.create(CreationRequest.model_validate(VALID_PAYLOAD))
    return created.generation_id


def test_trend_refresh_writes_back_to_database(monkeypatch) -> None:
    reset_database()
    repository = TrendTemplateRepository()
    template = repository.get_best_match(platform="bilibili", content_type="science_popularization")
    assert template is not None

    refreshed_template = template.model_copy(
        update={
            "summary": "数据库真值层已经写入新的趋势摘要。",
            "source_type": "manual_refresh_collected",
            "updated_at": datetime(2026, 3, 25, 8, 40, tzinfo=UTC),
        }
    )

    monkeypatch.setattr(
        "app.services.trend_strategy.service.trend_collector_service.refresh_templates",
        lambda refreshed_at: ([refreshed_template], "manual_refresh_collected"),
    )

    response = trend_strategy_service.refresh_templates()
    persisted = repository.get_best_match(platform="bilibili", content_type="science_popularization")

    assert response.source_type == "manual_refresh_collected"
    assert persisted is not None
    assert persisted.summary == "数据库真值层已经写入新的趋势摘要。"
    assert persisted.source_type == "manual_refresh_collected"


def test_trend_refresh_fallback_does_not_overwrite_existing_database_truth(monkeypatch) -> None:
    reset_database()
    repository = TrendTemplateRepository()
    original = repository.get_best_match(platform="bilibili", content_type="science_popularization")
    assert original is not None

    monkeypatch.setattr(
        "app.services.trend_strategy.service.trend_collector_service.refresh_templates",
        lambda refreshed_at: ([], "manual_refresh_fallback"),
    )

    response = trend_strategy_service.refresh_templates()
    persisted = repository.get_best_match(platform="bilibili", content_type="science_popularization")

    assert response.source_type == "manual_refresh_fallback"
    assert persisted is not None
    assert persisted.summary == original.summary
    assert persisted.source_type == original.source_type


def test_generate_status_result_export_chain_remains_stable_with_persistent_store(monkeypatch) -> None:
    reset_database()
    generation_materialization_coordinator.result_repository = SqlAlchemyGenerationResultRepository()
    monkeypatch.setattr(
        "app.services.generation_pipeline.coordinator.generation_execution_orchestrator.execute",
        lambda record: build_stub_result(record.generation_id),
    )
    generation_id = create_generation()
    generation_execution_runner.submit(generation_id)

    status_response = get_generation_status(generation_id)
    assert status_response.generation_id == generation_id

    mark_generation_done(generation_id)

    reloaded_store = GenerationPipelineStore()
    reloaded_status = reloaded_store.get_status(generation_id)
    assert reloaded_status.status == "PACKAGE_ASSEMBLING"

    result_response = get_generation_result(generation_id)
    result_payload = result_response.model_dump(mode="json")
    assert result_payload["result_package"]["overview"]["target_platform"] == "bilibili"

    cached_result = SqlAlchemyGenerationResultRepository().get(generation_id)
    assert cached_result is not None
    assert cached_result.result_package.overview["target_platform"] == "bilibili"
    final_status = GenerationPipelineStore().get_status(generation_id)
    assert final_status.status == "DONE"

    second_result_response = get_generation_result(generation_id)
    assert second_result_response.model_dump(mode="json") == result_payload

    json_export = export_generation_json(generation_id)
    assert json_export.model_dump(mode="json") == result_payload

    markdown_export = export_generation_markdown(generation_id)
    assert result_payload["result_package"]["overview"]["main_title"] in markdown_export

    video_payload = export_video_payload(generation_id)
    assert video_payload.video_meta["platform"] == "bilibili"


def test_status_does_not_fake_progress_before_execution_starts() -> None:
    reset_database()
    generation_id = create_generation()

    generation_pipeline_store.repository.update_created_at(
        generation_id,
        datetime.now(UTC) - timedelta(seconds=10),
    )

    status_response = get_generation_status(generation_id)
    assert str(status_response.status) == "THEME_PARSING"
    assert str(status_response.current_stage) == "THEME_PARSING"
    assert status_response.stage_message == "正在解析创作主题"
