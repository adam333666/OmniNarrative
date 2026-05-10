from __future__ import annotations

from sqlalchemy import Column, DateTime, Integer, JSON, String, Text, UniqueConstraint

from app.db.base import Base


class TrendTemplateModel(Base):
    __tablename__ = "platform_trend_templates"
    __table_args__ = (
        UniqueConstraint("platform", "content_type", name="uq_platform_content_type"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    platform = Column(String(64), nullable=False, index=True)
    content_type = Column(String(64), nullable=False, index=True, default="auto")
    summary = Column(Text, nullable=False)
    hook_patterns = Column(JSON, nullable=False)
    rhythm_patterns = Column(JSON, nullable=False)
    title_cover_style = Column(JSON, nullable=False)
    audience_preference_summary = Column(Text, nullable=False)
    avoid_patterns = Column(JSON, nullable=False)
    hot_topics_summary = Column(JSON, nullable=False)
    interaction_patterns = Column(JSON, nullable=False, default=list)
    emotional_entry_points = Column(JSON, nullable=False, default=list)
    creator_angle_summary = Column(Text, nullable=False, default="")
    source_trace = Column(JSON, nullable=False, default=list)
    source_type = Column(String(32), nullable=False, default="seed")
    updated_at = Column(DateTime(timezone=True), nullable=True)
