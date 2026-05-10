from __future__ import annotations

import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

TEST_DB_PATH = Path("/tmp/multi_media_m70_concurrency.db")
os.environ.setdefault("DATABASE_URL", f"sqlite+pysqlite:///{TEST_DB_PATH}")

from app.core.config import settings
from app.db.bootstrap import bootstrap_database
from app.db.repositories.generation_job_event_repository import SqlAlchemyGenerationJobEventRepository
from app.db.repositories.generation_job_repository import SqlAlchemyGenerationJobRepository
from app.db.repositories.generation_result_repository import SqlAlchemyGenerationResultRepository
from app.db.session import get_engine, get_session_factory
from app.schemas.creation_request import CreationRequest
from app.services.generation_pipeline.coordinator import generation_materialization_coordinator
from app.services.generation_pipeline.result_builder import generation_result_builder
from app.services.generation_pipeline.runner import generation_execution_runner
from app.services.generation_pipeline.store import generation_pipeline_store
from tests.test_m46_export_payload_compat import build_result as build_export_ready_result


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
    return CreationRequest(
        theme_text="时间旅行悖论",
        content_type="science_popularization",
        target_platform="bilibili",
        target_audience_text="18到28岁，喜欢科幻设定和逻辑推理的观众",
        style_tone="suspense",
        custom_style_text="保持一点烧脑感",
    )


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


def test_materialization_coordinator_serializes_concurrent_builds(monkeypatch) -> None:
    reset_database()
    created = generation_pipeline_store.create(build_request())
    call_count = 0
    call_lock = threading.Lock()

    def fake_execute(record):
        nonlocal call_count
        with call_lock:
            call_count += 1
        time.sleep(0.2)
        return build_stub_result(record.generation_id)

    monkeypatch.setattr(
        "app.services.generation_pipeline.coordinator.generation_execution_orchestrator.execute",
        fake_execute,
    )

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(
                generation_materialization_coordinator.materialize,
                created.generation_id,
                allow_pending_start=True,
            )
            for _ in range(4)
        ]
        results = [future.result() for future in futures]

    events = generation_pipeline_store.list_events(created.generation_id)
    completed_events = [event for event in events if event.event_type == "COMPLETED"]

    assert call_count == 1
    assert len({result.export_meta["generation_id"] for result in results}) == 1
    assert len(completed_events) == 1
    assert str(generation_pipeline_store.get_status(created.generation_id).status) == "DONE"


def test_runner_dedupes_concurrent_submissions_for_same_generation(monkeypatch) -> None:
    reset_database()
    created = generation_pipeline_store.create(build_request())
    monkeypatch.setattr(settings, "generation_auto_start_enabled", True)

    submitted_generation_ids: list[str] = []
    done_callbacks = []

    class PendingFuture:
        def add_done_callback(self, callback):
            done_callbacks.append(callback)

    class PendingExecutor:
        def submit(self, fn, generation_id):
            submitted_generation_ids.append(generation_id)
            return PendingFuture()

    monkeypatch.setattr(generation_execution_runner, "_get_executor", lambda: PendingExecutor())

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(generation_execution_runner.submit, created.generation_id) for _ in range(5)]
        results = [future.result() for future in futures]

    events = generation_pipeline_store.list_events(created.generation_id)

    assert results.count(True) == 1
    assert results.count(False) == 4
    assert submitted_generation_ids == [created.generation_id]
    assert created.generation_id in generation_execution_runner._inflight
    assert [event.event_type for event in events].count("BACKGROUND_SUBMITTED") == 1
    assert [event.event_type for event in events].count("BACKGROUND_DEDUPED") == 4

    for callback in done_callbacks:
        callback(None)

    assert created.generation_id not in generation_execution_runner._inflight
