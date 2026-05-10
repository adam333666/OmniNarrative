from __future__ import annotations

from datetime import datetime
from threading import Lock

from fastapi import HTTPException

from app.core.enums import GenerationStatus
from app.db.repositories.generation_result_repository import SqlAlchemyGenerationResultRepository
from app.schemas.narrative_package import ResultEnvelope
from app.services.generation_pipeline.checkpointer import generation_checkpoint_service
from app.services.generation_pipeline.orchestrator import generation_execution_orchestrator
from app.services.generation_pipeline.store import generation_pipeline_store


class GenerationMaterializationCoordinator:
    def __init__(self, result_repository: SqlAlchemyGenerationResultRepository | None = None) -> None:
        self.result_repository = result_repository or SqlAlchemyGenerationResultRepository()
        self._index_lock = Lock()
        self._locks: dict[str, Lock] = {}

    def materialize(self, generation_id: str, *, allow_pending_start: bool) -> ResultEnvelope:
        with self._get_lock(generation_id):
            status = generation_pipeline_store.get_status(generation_id)
            cached_result = self.result_repository.get(generation_id)
            if cached_result is not None:
                if status.status != GenerationStatus.done:
                    generation_pipeline_store.mark_done(generation_id)
                return cached_result

            if status.status in {GenerationStatus.package_assembling, GenerationStatus.done}:
                checkpoint_result = generation_checkpoint_service.get_latest_result_snapshot(generation_id)
                if checkpoint_result is not None:
                    saved_from_checkpoint = self.result_repository.save(
                        generation_id=generation_id,
                        result=checkpoint_result,
                        generated_at=datetime.fromisoformat(checkpoint_result.export_meta["generated_at"]),
                    )
                    generation_pipeline_store.mark_done(generation_id)
                    return saved_from_checkpoint

            if status.status in {GenerationStatus.failed, GenerationStatus.timeout}:
                raise HTTPException(status_code=409, detail="Generation can not be materialized from a terminal failure state")

            if not allow_pending_start and status.status not in {GenerationStatus.package_assembling, GenerationStatus.done}:
                raise HTTPException(status_code=409, detail="Generation is not finished yet")

            record = generation_pipeline_store.get_record(generation_id)
            result = generation_execution_orchestrator.execute(record)
            saved = self.result_repository.save(
                generation_id=generation_id,
                result=result,
                generated_at=datetime.fromisoformat(result.export_meta["generated_at"]),
            )
            generation_pipeline_store.mark_done(generation_id)
            return saved

    def _get_lock(self, generation_id: str) -> Lock:
        with self._index_lock:
            lock = self._locks.get(generation_id)
            if lock is None:
                lock = Lock()
                self._locks[generation_id] = lock
            return lock


generation_materialization_coordinator = GenerationMaterializationCoordinator()
