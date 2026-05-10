import os
from pathlib import Path

import pytest
from fastapi import HTTPException

TEST_DB_PATH = Path("/tmp/multi_media_test.db")
os.environ.setdefault("DATABASE_URL", f"sqlite+pysqlite:///{TEST_DB_PATH}")
os.environ.setdefault("INTERNAL_API_KEY", "change-me")

from app.api.routes.config import get_input_options, get_trend_templates, refresh_trend_templates
from app.api.routes.creations import (
    export_generation_markdown,
    export_video_payload,
    generate_creation,
    get_generation_result,
)
from app.core.config import settings
from app.db.bootstrap import bootstrap_database
from app.db.repositories.generation_job_event_repository import SqlAlchemyGenerationJobEventRepository
from app.db.repositories.generation_job_repository import SqlAlchemyGenerationJobRepository
from app.db.repositories.generation_result_repository import SqlAlchemyGenerationResultRepository
from app.db.session import get_engine, get_session_factory
from app.schemas.creation_request import CreationRequest
from app.services.generation_pipeline.runner import generation_execution_runner
from app.services.generation_pipeline.result_builder import generation_result_builder
from app.services.generation_pipeline.store import GenerationPipelineStore, generation_pipeline_store
from app.services.trend_strategy.service import trend_strategy_service
from app.services.trend_strategy.repository import TrendTemplateRepository


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
    generation_result_builder.result_repository = SqlAlchemyGenerationResultRepository()
    trend_strategy_service.repository = TrendTemplateRepository()
    settings.internal_api_key = "change-me"
    settings.generation_auto_start_enabled = True


@pytest.fixture(autouse=True)
def isolate_state() -> None:
    reset_database()


def mark_generation_done(generation_id: str) -> None:
    GenerationPipelineStore().mark_ready_for_result(generation_id)


def build_request(**overrides: str | None) -> CreationRequest:
    payload = {**VALID_PAYLOAD, **overrides}
    return CreationRequest.model_validate(payload)


def test_invalid_input_is_rejected() -> None:
    with pytest.raises(HTTPException) as exc_info:
        generate_creation(build_request(content_type="unsupported-mode"))

    assert exc_info.value.status_code == 422
    assert exc_info.value.detail == "Unsupported content_type"


def test_trend_templates_can_be_listed_and_refreshed() -> None:
    list_payload = get_trend_templates(platform=None, content_type=None)
    assert list_payload.total >= 5
    assert any(item.platform == "bilibili" for item in list_payload.items)

    refresh_payload = refresh_trend_templates(x_internal_api_key="change-me")
    assert refresh_payload.refreshed_count >= 5
    assert refresh_payload.source_type in {"manual_refresh_collected", "manual_refresh_fallback"}


def test_input_options_match_backend_supported_enums() -> None:
    payload = get_input_options()

    style_tones = {item["value"] for item in payload["style_tones"]}
    assert {
        "suspense",
        "healing",
        "passionate",
        "serious",
        "light",
        "twist",
        "high_emotion",
        "calm",
        "inspirational",
        "mysterious",
    } == style_tones


def test_result_envelope_matches_expected_shape(monkeypatch) -> None:
    monkeypatch.setattr(
        "app.api.routes.creations.generation_execution_runner.submit",
        lambda generation_id: True,
    )
    generate_response = generate_creation(build_request())
    generation_id = generate_response.generation_id

    mark_generation_done(generation_id)

    payload = get_generation_result(generation_id)

    assert "analysis" in payload.model_dump()
    assert "result_package" in payload.model_dump()
    assert "overview" in payload.result_package.model_dump()
    assert "script_layer" in payload.result_package.model_dump()
    assert payload.result_package.overview["target_platform"] == "bilibili"


def test_export_and_video_payload_endpoints_work(monkeypatch) -> None:
    monkeypatch.setattr(
        "app.api.routes.creations.generation_execution_runner.submit",
        lambda generation_id: True,
    )
    generate_response = generate_creation(build_request())
    generation_id = generate_response.generation_id

    mark_generation_done(generation_id)

    result_payload = get_generation_result(generation_id)

    markdown = export_generation_markdown(generation_id)
    assert "多模态叙事结果包" in markdown
    assert result_payload.result_package.overview["main_title"] in markdown

    payload = export_video_payload(generation_id)
    assert "video_meta" in payload.model_dump()
    assert "segments" in payload.model_dump()
    assert "negative_constraints" in payload.model_dump()
    assert payload.video_meta["title"] == result_payload.result_package.overview["main_title"]
    assert payload.video_meta["platform"] == result_payload.request_summary["target_platform"]
    assert payload.segments == result_payload.result_package.script_layer["segments"]
    assert payload.shots == result_payload.result_package.script_layer["key_shots"]
    assert payload.subtitle_blocks == [
        segment["subtitle_text"] for segment in result_payload.result_package.script_layer["segments"]
    ]
    assert payload.negative_constraints == result_payload.result_package.machine_payload_layer["negative_constraints"]
