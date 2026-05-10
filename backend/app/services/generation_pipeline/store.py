from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from fastapi import HTTPException

from app.core.enums import GenerationStatus
from app.db.repositories.generation_job_event_repository import GenerationJobEventRecord, SqlAlchemyGenerationJobEventRepository
from app.db.repositories.generation_result_repository import SqlAlchemyGenerationResultRepository
from app.db.repositories.generation_job_repository import SqlAlchemyGenerationJobRepository
from app.schemas.creation_request import CreationRequest
from app.schemas.generation import GenerationRecord
from app.schemas.status import GenerationStatusResponse

STAGE_SEQUENCE: list[tuple[GenerationStatus, str]] = [
    (GenerationStatus.theme_parsing, "正在解析创作主题"),
    (GenerationStatus.profile_parsing, "正在抽取受众与风格标签"),
    (GenerationStatus.trend_adapting, "正在进行平台与趋势适配"),
    (GenerationStatus.narrative_generating, "正在生成叙事骨架"),
    (GenerationStatus.package_assembling, "正在组装多模态内容包"),
]
STAGE_ORDER = {
    status: index
    for index, (status, _message) in enumerate(STAGE_SEQUENCE)
}

MAX_LIFETIME_SECONDS = 180


class GenerationPipelineStore:
    def __init__(
        self,
        repository: SqlAlchemyGenerationJobRepository | None = None,
        result_repository: SqlAlchemyGenerationResultRepository | None = None,
        event_repository: SqlAlchemyGenerationJobEventRepository | None = None,
    ) -> None:
        self.repository = repository or SqlAlchemyGenerationJobRepository()
        self.result_repository = result_repository or SqlAlchemyGenerationResultRepository()
        self.event_repository = event_repository or SqlAlchemyGenerationJobEventRepository()

    def create(self, request: CreationRequest) -> GenerationRecord:
        created_at = datetime.now(UTC)
        initial_status, initial_message = STAGE_SEQUENCE[0]
        record = GenerationRecord(
            generation_id=f"gen_{uuid4().hex[:12]}",
            request=request,
            created_at=created_at,
            current_status=initial_status,
            current_stage=initial_status,
            stage_message=initial_message,
            updated_at=created_at,
        )
        created = self.repository.create(record)
        self._append_event(
            generation_id=created.generation_id,
            event_type="CREATED",
            status=created.current_status,
            stage=created.current_stage,
            stage_message=created.stage_message,
            error_message=None,
            occurred_at=created.created_at,
        )
        return created

    def get_record(self, generation_id: str) -> GenerationRecord:
        record = self.repository.get(generation_id)
        if record is None:
            raise HTTPException(status_code=404, detail="Generation not found")
        return record

    def get_status(self, generation_id: str) -> GenerationStatusResponse:
        record = self._sync_status(generation_id)
        created_at = record.created_at if record.created_at.tzinfo is not None else record.created_at.replace(tzinfo=UTC)
        updated_at = (
            record.updated_at if record.updated_at is None or record.updated_at.tzinfo is not None else record.updated_at.replace(tzinfo=UTC)
        )
        completed_at = (
            record.completed_at if record.completed_at is None or record.completed_at.tzinfo is not None else record.completed_at.replace(tzinfo=UTC)
        )
        reference_time = completed_at or datetime.now(UTC)
        total_elapsed_seconds = max(int((reference_time - created_at).total_seconds()), 0)
        stage_elapsed_seconds = (
            max(int((reference_time - updated_at).total_seconds()), 0)
            if updated_at is not None
            else None
        )
        return GenerationStatusResponse(
            generation_id=generation_id,
            status=record.current_status,
            current_stage=record.current_stage,
            stage_message=record.stage_message,
            error_message=record.failure_reason,
            created_at=created_at,
            updated_at=updated_at,
            completed_at=completed_at,
            total_elapsed_seconds=total_elapsed_seconds,
            stage_elapsed_seconds=stage_elapsed_seconds,
        )

    def mark_done(self, generation_id: str, *, completed_at: datetime | None = None) -> GenerationRecord:
        record = self.repository.mark_done(
            generation_id,
            completed_at=completed_at or datetime.now(UTC),
            stage_message="多模态内容包已完成组装",
        )
        if record is None:
            raise HTTPException(status_code=404, detail="Generation not found")
        self._append_event(
            generation_id=record.generation_id,
            event_type="COMPLETED",
            status=record.current_status,
            stage=record.current_stage,
            stage_message=record.stage_message,
            error_message=None,
            occurred_at=record.completed_at or datetime.now(UTC),
        )
        return record

    def mark_stage(
        self,
        generation_id: str,
        *,
        stage_status: GenerationStatus,
        stage_message: str,
        updated_at: datetime | None = None,
    ) -> GenerationRecord:
        record = self.repository.update_stage(
            generation_id,
            current_status=stage_status,
            current_stage=stage_status,
            stage_message=stage_message,
            updated_at=updated_at or datetime.now(UTC),
        )
        if record is None:
            raise HTTPException(status_code=404, detail="Generation not found")
        event_type = "READY_FOR_RESULT" if stage_status == GenerationStatus.package_assembling else "STAGE_UPDATED"
        self._append_event(
            generation_id=record.generation_id,
            event_type=event_type,
            status=record.current_status,
            stage=record.current_stage,
            stage_message=record.stage_message,
            error_message=None,
            occurred_at=record.updated_at or datetime.now(UTC),
        )
        return record

    def mark_ready_for_result(self, generation_id: str, *, updated_at: datetime | None = None) -> GenerationRecord:
        return self.mark_stage(
            generation_id,
            stage_status=GenerationStatus.package_assembling,
            stage_message="正在组装多模态内容包",
            updated_at=updated_at,
        )

    def mark_failed(self, generation_id: str, *, error_message: str) -> GenerationRecord:
        existing = self.get_record(generation_id)
        failed_stage = existing.current_stage
        failed_stage_message = existing.stage_message
        record = self.repository.mark_failed(
            generation_id,
            error_message=error_message,
            updated_at=datetime.now(UTC),
            stage_message=f"在{failed_stage_message}阶段失败",
        )
        if record is None:
            raise HTTPException(status_code=404, detail="Generation not found")
        record.current_stage = failed_stage
        self._append_event(
            generation_id=record.generation_id,
            event_type="FAILED",
            status=record.current_status,
            stage=record.current_stage,
            stage_message=record.stage_message,
            error_message=record.failure_reason,
            occurred_at=record.updated_at or datetime.now(UTC),
        )
        return record

    def mark_timeout(self, generation_id: str, *, error_message: str = "Generation exceeded the allowed time window.") -> GenerationRecord:
        existing = self.get_record(generation_id)
        timeout_stage = existing.current_stage
        timeout_stage_message = existing.stage_message
        record = self.repository.mark_timeout(
            generation_id,
            updated_at=datetime.now(UTC),
            error_message=error_message,
            stage_message=f"在{timeout_stage_message}阶段超时",
        )
        if record is None:
            raise HTTPException(status_code=404, detail="Generation not found")
        record.current_stage = timeout_stage
        self._append_event(
            generation_id=record.generation_id,
            event_type="TIMEOUT",
            status=record.current_status,
            stage=record.current_stage,
            stage_message=record.stage_message,
            error_message=record.failure_reason,
            occurred_at=record.updated_at or datetime.now(UTC),
        )
        return record

    def _sync_status(self, generation_id: str) -> GenerationRecord:
        record = self.get_record(generation_id)
        if record.current_status in {GenerationStatus.done, GenerationStatus.failed, GenerationStatus.timeout}:
            return record

        if record.current_status == GenerationStatus.package_assembling and self.result_repository.get(generation_id) is not None:
            return self.mark_done(generation_id)

        created_at = record.created_at if record.created_at.tzinfo is not None else record.created_at.replace(tzinfo=UTC)
        now = datetime.now(UTC)
        elapsed_seconds = int((now - created_at).total_seconds())

        if record.failed:
            return self.mark_failed(generation_id, error_message=record.failure_reason or "Generation failed unexpectedly.")

        if elapsed_seconds >= MAX_LIFETIME_SECONDS or record.timed_out:
            return self.mark_timeout(generation_id)

        execution_has_started = self.event_repository.has_event_types(
            generation_id,
            [
                "BACKGROUND_SUBMITTED",
                "BACKGROUND_STARTED",
                "READY_FOR_RESULT",
                "STAGE_UPDATED",
                "COMPLETED",
                "FAILED",
                "TIMEOUT",
            ],
        )
        if not execution_has_started:
            return record

        # Once execution has started, only persisted stage transitions are trusted.
        # This prevents the status API from racing ahead of the real background work.
        return record

    def list_events(
        self,
        generation_id: str,
        *,
        event_type: str | None = None,
        limit: int | None = None,
        since: datetime | None = None,
        until: datetime | None = None,
        failed_only: bool = False,
    ) -> list[GenerationJobEventRecord]:
        self.get_record(generation_id)
        return self.event_repository.list_events(
            generation_id,
            event_type=event_type,
            limit=limit,
            since=since,
            until=until,
            failed_only=failed_only,
        )

    def record_event(
        self,
        generation_id: str,
        *,
        event_type: str,
        error_message: str | None = None,
        stage_message: str | None = None,
        occurred_at: datetime | None = None,
    ) -> GenerationRecord:
        record = self.get_record(generation_id)
        self._append_event(
            generation_id=record.generation_id,
            event_type=event_type,
            status=record.current_status,
            stage=record.current_stage,
            stage_message=stage_message or record.stage_message,
            error_message=error_message,
            occurred_at=occurred_at or datetime.now(UTC),
        )
        return record

    def _append_event(
        self,
        *,
        generation_id: str,
        event_type: str,
        status: str,
        stage: str,
        stage_message: str,
        error_message: str | None,
        occurred_at: datetime,
    ) -> None:
        self.event_repository.append_event(
            GenerationJobEventRecord(
                generation_id=generation_id,
                event_type=event_type,
                status=status,
                stage=stage,
                stage_message=stage_message,
                error_message=error_message,
                occurred_at=occurred_at,
            )
        )


generation_pipeline_store = GenerationPipelineStore()
