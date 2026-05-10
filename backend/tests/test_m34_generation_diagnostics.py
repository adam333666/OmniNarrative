from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

TEST_DB_PATH = Path("/tmp/multi_media_m34_diagnostics.db")
os.environ.setdefault("DATABASE_URL", f"sqlite+pysqlite:///{TEST_DB_PATH}")
os.environ.setdefault("INTERNAL_API_KEY", "change-me")

import pytest

from fastapi import HTTPException

from app.api.routes.creations import get_generation_diagnostics, get_generation_result
from app.core.config import settings
from app.schemas.creation_request import CreationRequest
from app.db.bootstrap import bootstrap_database
from app.db.repositories.generation_job_event_repository import SqlAlchemyGenerationJobEventRepository
from app.db.repositories.generation_job_repository import SqlAlchemyGenerationJobRepository
from app.db.repositories.generation_result_repository import SqlAlchemyGenerationResultRepository
from app.db.session import get_engine, get_session_factory
from app.services.generation_pipeline.coordinator import generation_materialization_coordinator
from app.services.generation_pipeline.runner import generation_execution_runner
from app.services.generation_pipeline.result_builder import generation_result_builder
from app.services.generation_pipeline.store import generation_pipeline_store
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
        TEST_DB_PATH.unlink(missing_ok=True)
    get_engine.cache_clear()
    get_session_factory.cache_clear()
    generation_execution_runner.shutdown(wait=False)
    bootstrap_database()
    generation_pipeline_store.repository = SqlAlchemyGenerationJobRepository()
    generation_pipeline_store.result_repository = SqlAlchemyGenerationResultRepository()
    generation_pipeline_store.event_repository = SqlAlchemyGenerationJobEventRepository()
    generation_result_builder.result_repository = SqlAlchemyGenerationResultRepository()
    generation_materialization_coordinator.result_repository = SqlAlchemyGenerationResultRepository()
    settings.internal_api_key = "change-me"
    settings.generation_auto_start_enabled = False


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


def test_generation_diagnostics_endpoint_returns_status_and_event_trail(monkeypatch) -> None:
    reset_database()
    monkeypatch.setattr(
        "app.services.generation_pipeline.coordinator.generation_execution_orchestrator.execute",
        lambda record: build_stub_result(record.generation_id),
    )
    generation_id = create_generation()
    generation_execution_runner.submit(generation_id)

    generation_pipeline_store.mark_ready_for_result(generation_id)
    result_response = get_generation_result(generation_id)
    assert result_response.export_meta["generation_id"] == generation_id

    payload = get_generation_diagnostics(
        generation_id,
        event_type=None,
        limit=None,
        since=None,
        until=None,
        failed_only=False,
        x_internal_api_key="change-me",
    )
    payload = payload.model_dump(mode="json")

    assert payload["generation_id"] == generation_id
    assert payload["status_snapshot"]["status"] == "DONE"
    assert payload["has_result_snapshot"] is True
    assert payload["event_count"] >= 4
    assert [item["event_type"] for item in payload["events"]][:3] == [
        "CREATED",
        "BACKGROUND_SKIPPED_DISABLED",
        "READY_FOR_RESULT",
    ]
    assert payload["events"][-1]["event_type"] == "COMPLETED"


def test_generation_diagnostics_endpoint_requires_internal_api_key() -> None:
    reset_database()
    generation_id = create_generation()

    with pytest.raises(HTTPException) as exc_info:
        get_generation_diagnostics(
            generation_id,
            event_type=None,
            limit=None,
            since=None,
            until=None,
            failed_only=False,
            x_internal_api_key="",
        )
    assert exc_info.value.status_code == 403


def test_generation_diagnostics_endpoint_can_filter_event_type_and_limit(monkeypatch) -> None:
    reset_database()
    monkeypatch.setattr(
        "app.services.generation_pipeline.coordinator.generation_execution_orchestrator.execute",
        lambda record: build_stub_result(record.generation_id),
    )
    generation_id = create_generation()
    generation_execution_runner.submit(generation_id)

    generation_pipeline_store.mark_ready_for_result(generation_id)
    get_generation_result(generation_id)

    payload = get_generation_diagnostics(
        generation_id,
        event_type="COMPLETED",
        limit=1,
        since=None,
        until=None,
        failed_only=False,
        x_internal_api_key="change-me",
    )
    payload = payload.model_dump(mode="json")
    assert payload["event_count"] == 1
    assert [item["event_type"] for item in payload["events"]] == ["COMPLETED"]


def test_generation_diagnostics_endpoint_can_filter_by_time_window(monkeypatch) -> None:
    reset_database()
    monkeypatch.setattr(
        "app.services.generation_pipeline.coordinator.generation_execution_orchestrator.execute",
        lambda record: build_stub_result(record.generation_id),
    )
    generation_id = create_generation()
    generation_execution_runner.submit(generation_id)

    generation_pipeline_store.mark_ready_for_result(generation_id)
    get_generation_result(generation_id)

    payload = get_generation_diagnostics(
        generation_id,
        event_type=None,
        limit=None,
        since=None,
        until=None,
        failed_only=False,
        x_internal_api_key="change-me",
    ).model_dump(mode="json")
    first_event_time = payload["events"][0]["occurred_at"]

    filtered_payload = get_generation_diagnostics(
        generation_id,
        event_type=None,
        limit=None,
        since=datetime.fromisoformat(first_event_time),
        until=None,
        failed_only=False,
        x_internal_api_key="change-me",
    )
    filtered_payload = filtered_payload.model_dump(mode="json")
    assert filtered_payload["event_count"] >= 1


def test_generation_diagnostics_endpoint_can_focus_on_failure_events() -> None:
    reset_database()
    generation_id = create_generation()

    generation_pipeline_store.mark_failed(generation_id, error_message="forced failure for diagnostics")

    payload = get_generation_diagnostics(
        generation_id,
        event_type=None,
        limit=None,
        since=None,
        until=None,
        failed_only=True,
        x_internal_api_key="change-me",
    )
    payload = payload.model_dump(mode="json")
    assert payload["event_count"] == 1
    assert payload["events"][0]["event_type"] == "FAILED"


def test_generation_diagnostics_endpoint_includes_background_skip_event_by_default() -> None:
    reset_database()
    generation_id = create_generation()
    generation_execution_runner.submit(generation_id)

    payload = get_generation_diagnostics(
        generation_id,
        event_type="BACKGROUND_SKIPPED_DISABLED",
        limit=None,
        since=None,
        until=None,
        failed_only=False,
        x_internal_api_key="change-me",
    )
    payload = payload.model_dump(mode="json")
    assert payload["event_count"] == 1
    assert payload["events"][0]["event_type"] == "BACKGROUND_SKIPPED_DISABLED"
