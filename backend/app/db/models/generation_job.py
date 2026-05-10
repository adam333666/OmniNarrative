from __future__ import annotations

from sqlalchemy import Boolean, Column, DateTime, Integer, JSON, String, Text, UniqueConstraint

from app.db.base import Base


class GenerationJobModel(Base):
    __tablename__ = "generation_jobs"
    __table_args__ = (
        UniqueConstraint("generation_id", name="uq_generation_jobs_generation_id"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    generation_id = Column(String(32), nullable=False, index=True)
    request_payload = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, index=True)
    current_status = Column(String(32), nullable=False, default="THEME_PARSING")
    current_stage = Column(String(32), nullable=False, default="THEME_PARSING")
    stage_message = Column(Text, nullable=False, default="正在解析创作主题")
    failed = Column(Boolean, nullable=False, default=False)
    timed_out = Column(Boolean, nullable=False, default=False)
    failure_reason = Column(Text, nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), nullable=False, index=True)
