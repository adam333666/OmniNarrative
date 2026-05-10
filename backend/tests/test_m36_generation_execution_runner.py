from __future__ import annotations

import os
from pathlib import Path

import pytest

TEST_DB_PATH = Path("/tmp/multi_media_test.db")
os.environ.setdefault("DATABASE_URL", f"sqlite+pysqlite:///{TEST_DB_PATH}")

from app.api.routes.creations import generate_creation
from app.core.config import settings
from fastapi import HTTPException
from app.db.bootstrap import bootstrap_database
from app.db.repositories.generation_job_event_repository import SqlAlchemyGenerationJobEventRepository
from app.db.repositories.generation_job_repository import SqlAlchemyGenerationJobRepository
from app.db.repositories.generation_result_repository import SqlAlchemyGenerationResultRepository
from app.db.session import get_engine, get_session_factory
from app.schemas.creation_request import CreationRequest
from app.schemas.narrative_package import ResultEnvelope
from app.services.generation_pipeline.coordinator import generation_materialization_coordinator
from app.services.generation_pipeline.result_builder import generation_result_builder
from app.services.generation_pipeline.runner import generation_execution_runner
from app.services.generation_pipeline.store import generation_pipeline_store


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
    generation_materialization_coordinator.result_repository = SqlAlchemyGenerationResultRepository()


def build_request() -> CreationRequest:
    return CreationRequest.model_validate(VALID_PAYLOAD)


def build_result(generation_id: str) -> ResultEnvelope:
    return ResultEnvelope.model_validate(
        {
            "request_summary": VALID_PAYLOAD,
            "analysis": {
                "audience_profile": {
                    "raw_text": VALID_PAYLOAD["target_audience_text"],
                    "age_group_guess": "18-24",
                    "interest_tags": ["脑洞设定"],
                    "pain_points": ["复杂概念理解门槛高"],
                    "content_preference": ["开头要快"],
                    "emotion_preference": ["希望被带入但不被说教"],
                },
                "style_profile": {
                    "style_label": VALID_PAYLOAD["style_tone"],
                    "emotion_label": "紧张好奇",
                    "intensity_level": "medium",
                    "custom_notes": VALID_PAYLOAD["custom_style_text"],
                },
                "trend_summary": {
                    "platform": "bilibili",
                    "content_type": "science_popularization",
                    "summary": "平台节奏偏强钩子",
                    "hook_patterns": ["先抛问题"],
                    "rhythm_patterns": ["快切进入"],
                    "title_cover_style": ["高信息密度", "强对比标题"],
                    "audience_preference_summary": "偏好高信息密度和快速进入主题的表达。",
                    "avoid_patterns": ["铺垫过长"],
                    "hot_topics_summary": ["时间悖论", "科幻设定拆解"],
                    "source_type": "db_truth",
                    "updated_at": "2026-03-27T00:00:00+00:00",
                },
                "key_design_decisions": ["先完整后优化"],
            },
            "result_package": {
                "overview": {"main_title": "时间旅行悖论，为什么会让人越想越上头？"},
                "script_layer": {"segments": [], "key_shots": []},
                "multimodal_layer": {},
                "platform_layer": {},
                "machine_payload_layer": {},
            },
            "export_meta": {
                "schema_version": "0.1.0",
                "generation_id": generation_id,
                "generated_at": "2026-03-27T00:00:00+00:00",
            },
        }
    )


def test_materialization_coordinator_can_start_from_fresh_job(monkeypatch) -> None:
    reset_database()
    created = generation_pipeline_store.create(build_request())

    monkeypatch.setattr(
        "app.services.generation_pipeline.coordinator.generation_execution_orchestrator.execute",
        lambda record: build_result(record.generation_id),
    )

    result = generation_materialization_coordinator.materialize(
        created.generation_id,
        allow_pending_start=True,
    )
    status = generation_pipeline_store.get_status(created.generation_id)
    events = generation_pipeline_store.list_events(created.generation_id)

    assert result.export_meta["generation_id"] == created.generation_id
    assert status.status == "DONE"
    assert events[-1].event_type == "COMPLETED"


def test_generate_route_submits_background_runner_when_enabled(monkeypatch) -> None:
    reset_database()
    submitted: list[str] = []

    monkeypatch.setattr(settings, "generation_auto_start_enabled", True)
    monkeypatch.setattr(
        "app.api.routes.creations.generation_execution_runner.submit",
        lambda generation_id: submitted.append(generation_id) or True,
    )

    response = generate_creation(build_request())

    generation_id = response.generation_id
    assert submitted == [generation_id]


def test_generate_route_rejects_requests_when_auto_start_disabled(monkeypatch) -> None:
    reset_database()
    monkeypatch.setattr(settings, "generation_auto_start_enabled", False)

    with pytest.raises(HTTPException) as exc_info:
        generate_creation(build_request())

    assert exc_info.value.status_code == 503
    assert exc_info.value.detail == "Generation auto-start is disabled in the current environment"


def test_generate_route_marks_job_failed_when_background_submit_crashes(monkeypatch) -> None:
    reset_database()
    monkeypatch.setattr(settings, "generation_auto_start_enabled", True)
    monkeypatch.setattr(
        "app.api.routes.creations.generation_execution_runner.submit",
        lambda generation_id: (_ for _ in ()).throw(RuntimeError("executor unavailable")),
    )

    with generation_pipeline_store.repository.session_factory() as session:
        from app.db.models.generation_job import GenerationJobModel

        before_ids = {item.generation_id for item in session.query(GenerationJobModel).all()}

    with pytest.raises(HTTPException) as exc_info:
        generate_creation(build_request())

    with generation_pipeline_store.repository.session_factory() as session:
        from app.db.models.generation_job import GenerationJobModel

        after_records = session.query(GenerationJobModel).all()
        created_records = [item for item in after_records if item.generation_id not in before_ids]

    assert exc_info.value.status_code == 503
    assert exc_info.value.detail == "Generation could not be scheduled for background execution"
    assert len(created_records) == 1
    failed_record = generation_pipeline_store.get_record(created_records[0].generation_id)
    events = generation_pipeline_store.list_events(created_records[0].generation_id)
    assert failed_record.current_status == "FAILED"
    assert failed_record.failure_reason == "executor unavailable"
    assert events[-1].event_type == "FAILED"


def test_runner_records_submission_start_and_dedup_events(monkeypatch) -> None:
    reset_database()
    created = generation_pipeline_store.create(build_request())
    monkeypatch.setattr(settings, "generation_auto_start_enabled", True)

    class InlineFuture:
        def add_done_callback(self, callback):
            callback(self)

    class InlineExecutor:
        def submit(self, fn, generation_id):
            fn(generation_id)
            return InlineFuture()

    monkeypatch.setattr(
        "app.services.generation_pipeline.runner.generation_materialization_coordinator.materialize",
        lambda generation_id, allow_pending_start: build_result(generation_id),
    )
    monkeypatch.setattr(generation_execution_runner, "_get_executor", lambda: InlineExecutor())

    submitted = generation_execution_runner.submit(created.generation_id)
    events = generation_pipeline_store.list_events(created.generation_id)

    assert submitted is True
    assert [event.event_type for event in events] == [
        "CREATED",
        "BACKGROUND_SUBMITTED",
        "BACKGROUND_STARTED",
    ]

    generation_execution_runner._inflight.add(created.generation_id)
    deduped = generation_execution_runner.submit(created.generation_id)
    events = generation_pipeline_store.list_events(created.generation_id)

    assert deduped is False
    assert events[-1].event_type == "BACKGROUND_DEDUPED"
    generation_execution_runner._inflight.discard(created.generation_id)


def test_runner_records_disabled_skip_event(monkeypatch) -> None:
    reset_database()
    created = generation_pipeline_store.create(build_request())

    monkeypatch.setattr(settings, "generation_auto_start_enabled", False)

    submitted = generation_execution_runner.submit(created.generation_id)
    events = generation_pipeline_store.list_events(created.generation_id)

    assert submitted is False
    assert events[-1].event_type == "BACKGROUND_SKIPPED_DISABLED"


def test_runner_shutdown_clears_inflight_generation_ids() -> None:
    reset_database()
    created = generation_pipeline_store.create(build_request())

    generation_execution_runner._inflight.add(created.generation_id)
    generation_execution_runner.shutdown(wait=False)

    assert created.generation_id not in generation_execution_runner._inflight


def test_runner_releases_inflight_when_submit_to_executor_fails(monkeypatch) -> None:
    reset_database()
    created = generation_pipeline_store.create(build_request())
    monkeypatch.setattr(settings, "generation_auto_start_enabled", True)

    class BrokenExecutor:
        def submit(self, fn, generation_id):
            raise RuntimeError("executor unavailable")

    monkeypatch.setattr(generation_execution_runner, "_get_executor", lambda: BrokenExecutor())

    with pytest.raises(RuntimeError) as exc_info:
        generation_execution_runner.submit(created.generation_id)

    events = generation_pipeline_store.list_events(created.generation_id)

    assert str(exc_info.value) == "executor unavailable"
    assert created.generation_id not in generation_execution_runner._inflight
    assert [event.event_type for event in events] == [
        "CREATED",
        "BACKGROUND_SUBMITTED",
        "BACKGROUND_SUBMIT_FAILED",
    ]
