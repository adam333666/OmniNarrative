from __future__ import annotations

from datetime import UTC, datetime

from fastapi import HTTPException

from app.core.enums import GenerationStatus
from app.schemas.narrative_package import ResultEnvelope
from app.services.generation_pipeline.checkpointer import generation_checkpoint_service
from app.services.generation_pipeline.store import generation_pipeline_store


class GenerationCheckpointRecoveryService:
    def restore_latest_result(self, generation_id: str) -> ResultEnvelope:
        record = generation_pipeline_store.get_record(generation_id)
        if record.current_status not in {
            GenerationStatus.package_assembling,
            GenerationStatus.done,
            GenerationStatus.failed,
            GenerationStatus.timeout,
        }:
            raise HTTPException(status_code=409, detail="Generation is not ready for checkpoint-based restoration")

        result = generation_checkpoint_service.get_latest_result_snapshot(generation_id)
        if result is None:
            raise HTTPException(status_code=404, detail="No checkpoint result snapshot found for generation")

        generated_at = datetime.fromisoformat(result.export_meta["generated_at"])
        generation_pipeline_store.result_repository.save(
            generation_id=generation_id,
            result=result,
            generated_at=generated_at if generated_at.tzinfo is not None else generated_at.replace(tzinfo=UTC),
        )
        generation_pipeline_store.mark_done(generation_id)
        return result


generation_checkpoint_recovery_service = GenerationCheckpointRecoveryService()
