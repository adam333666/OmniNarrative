from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from app.db.models.generation_job_event import GenerationJobEventModel
from app.db.session import get_session_factory


@dataclass(slots=True)
class GenerationJobEventRecord:
    generation_id: str
    event_type: str
    status: str
    stage: str
    stage_message: str
    error_message: str | None
    occurred_at: datetime


class SqlAlchemyGenerationJobEventRepository:
    def __init__(self, session_factory: sessionmaker[Session] | None = None) -> None:
        self.session_factory = session_factory or get_session_factory()

    def append_event(self, record: GenerationJobEventRecord) -> GenerationJobEventRecord:
        with self.session_factory() as session:
            session.add(
                GenerationJobEventModel(
                    generation_id=record.generation_id,
                    event_type=record.event_type,
                    status=record.status,
                    stage=record.stage,
                    stage_message=record.stage_message,
                    error_message=record.error_message,
                    occurred_at=record.occurred_at,
                )
            )
            session.commit()
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
        with self.session_factory() as session:
            statement = (
                select(GenerationJobEventModel)
                .where(GenerationJobEventModel.generation_id == generation_id)
                .order_by(GenerationJobEventModel.occurred_at, GenerationJobEventModel.id)
            )
            if event_type is not None:
                statement = statement.where(GenerationJobEventModel.event_type == event_type)
            if failed_only:
                statement = statement.where(GenerationJobEventModel.event_type.in_(["FAILED", "TIMEOUT"]))
            if since is not None:
                statement = statement.where(GenerationJobEventModel.occurred_at >= since)
            if until is not None:
                statement = statement.where(GenerationJobEventModel.occurred_at <= until)
            if limit is not None:
                statement = statement.limit(limit)
            return [self._to_record(item) for item in session.scalars(statement).all()]

    def has_event_types(self, generation_id: str, event_types: list[str]) -> bool:
        if not event_types:
            return False

        with self.session_factory() as session:
            statement = (
                select(GenerationJobEventModel.id)
                .where(GenerationJobEventModel.generation_id == generation_id)
                .where(GenerationJobEventModel.event_type.in_(event_types))
                .limit(1)
            )
            return session.scalar(statement) is not None

    def _to_record(self, model: GenerationJobEventModel) -> GenerationJobEventRecord:
        return GenerationJobEventRecord(
            generation_id=model.generation_id,
            event_type=model.event_type,
            status=model.status,
            stage=model.stage,
            stage_message=model.stage_message,
            error_message=model.error_message,
            occurred_at=model.occurred_at,
        )
