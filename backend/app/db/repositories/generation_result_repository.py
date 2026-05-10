from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from app.db.models.generation_result import GenerationResultModel
from app.db.session import get_session_factory
from app.schemas.narrative_package import ResultEnvelope


class SqlAlchemyGenerationResultRepository:
    def __init__(self, session_factory: sessionmaker[Session] | None = None) -> None:
        self.session_factory = session_factory or get_session_factory()

    def get(self, generation_id: str) -> ResultEnvelope | None:
        with self.session_factory() as session:
            statement = select(GenerationResultModel).where(GenerationResultModel.generation_id == generation_id)
            item = session.scalar(statement)
            if item is None:
                return None
            return ResultEnvelope.model_validate(item.result_payload)

    def save(self, generation_id: str, result: ResultEnvelope, generated_at: datetime) -> ResultEnvelope:
        with self.session_factory() as session:
            statement = select(GenerationResultModel).where(GenerationResultModel.generation_id == generation_id)
            item = session.scalar(statement)
            payload = result.model_dump(mode="json")
            if item is None:
                session.add(
                    GenerationResultModel(
                        generation_id=generation_id,
                        result_payload=payload,
                        generated_at=generated_at,
                    )
                )
            else:
                item.result_payload = payload
                item.generated_at = generated_at
                session.add(item)
            session.commit()
        return result
