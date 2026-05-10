from __future__ import annotations

import os
from datetime import timedelta
from pathlib import Path

TEST_DB_PATH = Path("/tmp/multi_media_m30_store.db")
os.environ.setdefault("DATABASE_URL", f"sqlite+pysqlite:///{TEST_DB_PATH}")

from app.db.bootstrap import bootstrap_database
from app.db.repositories.generation_job_repository import SqlAlchemyGenerationJobRepository
from app.db.session import get_engine, get_session_factory
from app.schemas.creation_request import CreationRequest
from app.services.generation_pipeline.store import GenerationPipelineStore


def reset_database() -> None:
    get_engine().dispose()
    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink()
    get_engine.cache_clear()
    get_session_factory.cache_clear()
    bootstrap_database()


def build_request() -> CreationRequest:
    return CreationRequest(
        theme_text="时间旅行悖论",
        content_type="science_popularization",
        target_platform="bilibili",
        target_audience_text="18到28岁，喜欢科幻设定和逻辑推理的观众",
        style_tone="suspense",
        custom_style_text="保持一点烧脑感",
    )


def test_generation_store_persists_record_and_can_be_reloaded() -> None:
    reset_database()
    store = GenerationPipelineStore()

    created = store.create(build_request())
    reloaded_store = GenerationPipelineStore()
    loaded = reloaded_store.get_record(created.generation_id)

    assert loaded.generation_id == created.generation_id
    assert loaded.request.theme_text == "时间旅行悖论"
    assert loaded.current_status == "THEME_PARSING"
    assert loaded.current_stage == "THEME_PARSING"
    assert loaded.stage_message == "正在解析创作主题"
    assert loaded.failed is False
    assert loaded.timed_out is False
    events = reloaded_store.list_events(created.generation_id)
    assert [event.event_type for event in events] == ["CREATED"]


def test_generation_status_is_consistent_across_store_instances() -> None:
    reset_database()
    store = GenerationPipelineStore()
    created = store.create(build_request())

    reloaded_store = GenerationPipelineStore()
    status = reloaded_store.get_status(created.generation_id)

    assert status.generation_id == created.generation_id
    assert status.status == "THEME_PARSING"
    assert status.current_stage == "THEME_PARSING"


def test_generation_status_sync_persists_advanced_stage_to_database() -> None:
    reset_database()
    store = GenerationPipelineStore()
    created = store.create(build_request())

    repository = SqlAlchemyGenerationJobRepository()
    repository.update_created_at(created.generation_id, created.created_at.replace(year=created.created_at.year - 1))
    synced_status = GenerationPipelineStore().get_status(created.generation_id)
    persisted = repository.get(created.generation_id)

    assert synced_status.status == "TIMEOUT"
    assert synced_status.current_stage == "THEME_PARSING"
    assert synced_status.stage_message == "在正在解析创作主题阶段超时"
    assert synced_status.total_elapsed_seconds is not None
    assert synced_status.stage_elapsed_seconds is not None
    assert persisted is not None
    assert persisted.current_status == "TIMEOUT"
    assert persisted.current_stage == "THEME_PARSING"
    assert persisted.stage_message == "在正在解析创作主题阶段超时"


def test_generation_status_does_not_fake_progress_after_background_submission() -> None:
    reset_database()
    store = GenerationPipelineStore()
    created = store.create(build_request())
    store.record_event(created.generation_id, event_type="BACKGROUND_SUBMITTED")

    repository = SqlAlchemyGenerationJobRepository()
    repository.update_created_at(created.generation_id, created.created_at.replace(minute=max(created.created_at.minute - 1, 0)))
    synced_status = GenerationPipelineStore().get_status(created.generation_id)
    persisted = repository.get(created.generation_id)

    assert synced_status.status == "THEME_PARSING"
    assert synced_status.current_stage == "THEME_PARSING"
    assert persisted is not None
    assert persisted.current_status == "THEME_PARSING"
    assert persisted.current_stage == "THEME_PARSING"


def test_generation_status_only_advances_when_stage_update_is_persisted() -> None:
    reset_database()
    store = GenerationPipelineStore()
    created = store.create(build_request())
    store.record_event(created.generation_id, event_type="BACKGROUND_SUBMITTED")

    repository = SqlAlchemyGenerationJobRepository()
    repository.update_created_at(created.generation_id, created.created_at - timedelta(seconds=4))

    synced_status = GenerationPipelineStore().get_status(created.generation_id)
    persisted = repository.get(created.generation_id)

    assert synced_status.status == "THEME_PARSING"
    assert synced_status.current_stage == "THEME_PARSING"
    assert persisted is not None
    assert persisted.current_status == "THEME_PARSING"
    assert persisted.current_stage == "THEME_PARSING"


def test_generation_store_returns_failed_status_with_saved_reason() -> None:
    reset_database()
    store = GenerationPipelineStore()
    created = store.create(build_request())

    store.mark_failed(created.generation_id, error_message="Model gateway unavailable.")

    status = GenerationPipelineStore().get_status(created.generation_id)
    events = GenerationPipelineStore().list_events(created.generation_id)

    assert status.status == "FAILED"
    assert status.current_stage == "THEME_PARSING"
    assert status.stage_message == "在正在解析创作主题阶段失败"
    assert status.error_message == "Model gateway unavailable."
    assert [event.event_type for event in events] == ["CREATED", "FAILED"]


def test_generation_store_records_event_trail_for_ready_and_done_transitions() -> None:
    reset_database()
    store = GenerationPipelineStore()
    created = store.create(build_request())

    store.mark_ready_for_result(created.generation_id)
    store.mark_done(created.generation_id)
    events = store.list_events(created.generation_id)

    assert [event.event_type for event in events] == ["CREATED", "READY_FOR_RESULT", "COMPLETED"]


def test_generation_store_raises_404_for_unknown_id() -> None:
    reset_database()
    store = GenerationPipelineStore()

    try:
        store.get_record("gen_missing")
    except Exception as exc:  # noqa: BLE001
        assert getattr(exc, "status_code", None) == 404
    else:
        raise AssertionError("Expected missing generation to raise 404")
