from __future__ import annotations

from sqlalchemy import Column, DateTime, Integer, JSON, String, UniqueConstraint

from app.db.base import Base


class GenerationResultModel(Base):
    __tablename__ = "generation_results"
    __table_args__ = (
        UniqueConstraint("generation_id", name="uq_generation_results_generation_id"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    generation_id = Column(String(32), nullable=False, index=True)
    result_payload = Column(JSON, nullable=False)
    generated_at = Column(DateTime(timezone=True), nullable=False, index=True)
