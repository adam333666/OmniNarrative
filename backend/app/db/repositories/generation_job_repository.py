from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from app.db.models.generation_job import GenerationJobModel
from app.db.session import get_session_factory
from app.schemas.generation import GenerationRecord


class SqlAlchemyGenerationJobRepository:
    def __init__(self, session_factory: sessionmaker[Session] | None = None) -> None:
        self.session_factory = session_factory or get_session_factory()

    def create(self, record: GenerationRecord) -> GenerationRecord:
        with self.session_factory() as session:
            payload = record.model_dump()
            payload["request_payload"] = payload.pop("request")
            session.add(GenerationJobModel(**payload))
            session.commit()
        return record

    def get(self, generation_id: str) -> GenerationRecord | None:
        with self.session_factory() as session:
            statement = select(GenerationJobModel).where(GenerationJobModel.generation_id == generation_id)
            item = session.scalar(statement)
            return self._to_schema(item) if item is not None else None

    def update_flags(
        self,
        generation_id: str,
        *,
        failed: bool | None = None,
        timed_out: bool | None = None,
        failure_reason: str | None = None,
    ) -> GenerationRecord | None:
        with self.session_factory() as session:
            statement = select(GenerationJobModel).where(GenerationJobModel.generation_id == generation_id)
            item = session.scalar(statement)
            if item is None:
                return None

            if failed is not None:
                item.failed = failed
            if timed_out is not None:
                item.timed_out = timed_out
            if failure_reason is not None:
                item.failure_reason = failure_reason

            session.add(item)
            session.commit()
            session.refresh(item)
            return self._to_schema(item)

    def update_stage(
        self,
        generation_id: str,
        *,
        current_status: str,
        current_stage: str,
        stage_message: str,
        updated_at: datetime,
    ) -> GenerationRecord | None:
        with self.session_factory() as session:
            statement = select(GenerationJobModel).where(GenerationJobModel.generation_id == generation_id)
            item = session.scalar(statement)
            if item is None:
                return None

            item.current_status = current_status
            item.current_stage = current_stage
            item.stage_message = stage_message
            item.updated_at = updated_at
            session.add(item)
            session.commit()
            session.refresh(item)
            return self._to_schema(item)

    def mark_done(self, generation_id: str, *, completed_at: datetime, stage_message: str) -> GenerationRecord | None:
        with self.session_factory() as session:
            statement = select(GenerationJobModel).where(GenerationJobModel.generation_id == generation_id)
            item = session.scalar(statement)
            if item is None:
                return None

            item.current_status = "DONE"
            item.current_stage = "DONE"
            item.stage_message = stage_message
            item.completed_at = completed_at
            item.updated_at = completed_at
            item.failed = False
            item.timed_out = False
            item.failure_reason = None
            session.add(item)
            session.commit()
            session.refresh(item)
            return self._to_schema(item)

    def mark_failed(
        self,
        generation_id: str,
        *,
        error_message: str,
        updated_at: datetime,
        stage_message: str | None = None,
    ) -> GenerationRecord | None:
        with self.session_factory() as session:
            statement = select(GenerationJobModel).where(GenerationJobModel.generation_id == generation_id)
            item = session.scalar(statement)
            if item is None:
                return None

            item.current_status = "FAILED"
            item.current_stage = item.current_stage or "THEME_PARSING"
            item.stage_message = stage_message or item.stage_message or "生成失败"
            item.failed = True
            item.timed_out = False
            item.failure_reason = error_message
            item.updated_at = updated_at
            session.add(item)
            session.commit()
            session.refresh(item)
            return self._to_schema(item)

    def mark_timeout(
        self,
        generation_id: str,
        *,
        updated_at: datetime,
        error_message: str,
        stage_message: str | None = None,
    ) -> GenerationRecord | None:
        with self.session_factory() as session:
            statement = select(GenerationJobModel).where(GenerationJobModel.generation_id == generation_id)
            item = session.scalar(statement)
            if item is None:
                return None

            item.current_status = "TIMEOUT"
            item.current_stage = item.current_stage or "THEME_PARSING"
            item.stage_message = stage_message or item.stage_message or "生成超时"
            item.failed = False
            item.timed_out = True
            item.failure_reason = error_message
            item.updated_at = updated_at
            session.add(item)
            session.commit()
            session.refresh(item)
            return self._to_schema(item)

    def update_created_at(self, generation_id: str, created_at: datetime) -> GenerationRecord | None:
        with self.session_factory() as session:
            statement = select(GenerationJobModel).where(GenerationJobModel.generation_id == generation_id)
            item = session.scalar(statement)
            if item is None:
                return None

            item.created_at = created_at
            item.updated_at = created_at if item.updated_at is None else item.updated_at
            session.add(item)
            session.commit()
            session.refresh(item)
            return self._to_schema(item)

    def _to_schema(self, model: GenerationJobModel) -> GenerationRecord:
        return GenerationRecord(
            generation_id=model.generation_id,
            request=model.request_payload,
            created_at=model.created_at,
            current_status=model.current_status,
            current_stage=model.current_stage,
            stage_message=model.stage_message,
            failed=model.failed,
            timed_out=model.timed_out,
            failure_reason=model.failure_reason,
            completed_at=model.completed_at,
            updated_at=model.updated_at,
        )
