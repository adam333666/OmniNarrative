from __future__ import annotations

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.db.base import Base


class GenerationJobEventModel(Base):
    __tablename__ = "generation_job_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    generation_id = Column(String(32), nullable=False, index=True)
    event_type = Column(String(32), nullable=False, index=True)
    status = Column(String(32), nullable=False)
    stage = Column(String(32), nullable=False)
    stage_message = Column(Text, nullable=False)
    error_message = Column(Text, nullable=True)
    occurred_at = Column(DateTime(timezone=True), nullable=False, index=True)
