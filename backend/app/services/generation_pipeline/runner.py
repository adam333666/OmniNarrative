from __future__ import annotations

from datetime import UTC, datetime
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

from app.core.config import settings
from app.core.enums import GenerationStatus
from app.services.generation_pipeline.coordinator import generation_materialization_coordinator
from app.services.generation_pipeline.store import generation_pipeline_store


class GenerationExecutionRunner:
    def __init__(self, max_workers: int | None = None) -> None:
        self.max_workers = max_workers or settings.generation_background_workers
        self.executor: ThreadPoolExecutor | None = None
        self._lock = Lock()
        self._inflight: set[str] = set()

    def submit(self, generation_id: str) -> bool:
        if not settings.generation_auto_start_enabled:
            generation_pipeline_store.record_event(
                generation_id,
                event_type="BACKGROUND_SKIPPED_DISABLED",
                stage_message="后台自动执行未启用，本次仅创建任务记录。",
            )
            return False

        status = generation_pipeline_store.get_status(generation_id)
        if status.status in {GenerationStatus.done, GenerationStatus.failed, GenerationStatus.timeout}:
            generation_pipeline_store.record_event(
                generation_id,
                event_type="BACKGROUND_SKIPPED_TERMINAL",
                stage_message="任务已处于终态，后台执行未再次提交。",
            )
            return False

        with self._lock:
            if generation_id in self._inflight:
                generation_pipeline_store.record_event(
                    generation_id,
                    event_type="BACKGROUND_DEDUPED",
                    stage_message="后台执行任务已在进行中，本次提交已去重。",
                )
                return False
            self._inflight.add(generation_id)

        generation_pipeline_store.record_event(
            generation_id,
            event_type="BACKGROUND_SUBMITTED",
            stage_message="任务已提交到后台执行器。",
        )
        try:
            future = self._get_executor().submit(self._run, generation_id)
        except Exception as exc:
            self._mark_finished(generation_id)
            generation_pipeline_store.record_event(
                generation_id,
                event_type="BACKGROUND_SUBMIT_FAILED",
                error_message=str(exc) or "Background generation could not be submitted.",
                stage_message="任务提交到后台执行器时失败。",
                occurred_at=datetime.now(UTC),
            )
            raise
        future.add_done_callback(lambda _: self._mark_finished(generation_id))
        return True

    def _run(self, generation_id: str) -> None:
        generation_pipeline_store.record_event(
            generation_id,
            event_type="BACKGROUND_STARTED",
            stage_message="后台执行器已开始处理任务。",
        )
        try:
            generation_materialization_coordinator.materialize(
                generation_id,
                allow_pending_start=True,
            )
        except Exception as exc:
            record = generation_pipeline_store.get_record(generation_id)
            if record.current_status not in {GenerationStatus.failed, GenerationStatus.timeout, GenerationStatus.done}:
                generation_pipeline_store.mark_failed(
                    generation_id,
                    error_message=str(exc) or "Background generation failed unexpectedly.",
                )
            generation_pipeline_store.record_event(
                generation_id,
                event_type="BACKGROUND_CRASHED",
                error_message=str(exc) or "Background generation failed unexpectedly.",
                stage_message="后台执行器在任务执行时崩溃。",
                occurred_at=datetime.now(UTC),
            )
            raise

    def _mark_finished(self, generation_id: str) -> None:
        with self._lock:
            self._inflight.discard(generation_id)

    def shutdown(self, *, wait: bool = False) -> None:
        with self._lock:
            executor = self.executor
            self.executor = None
            self._inflight.clear()
        if executor is not None:
            executor.shutdown(wait=wait, cancel_futures=False)

    def _get_executor(self) -> ThreadPoolExecutor:
        with self._lock:
            if self.executor is None:
                self.executor = ThreadPoolExecutor(
                    max_workers=self.max_workers,
                    thread_name_prefix="generation-exec",
                )
            return self.executor


generation_execution_runner = GenerationExecutionRunner()
