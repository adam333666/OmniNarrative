from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from app.db.models.trend_template import TrendTemplateModel
from app.db.session import get_session_factory
from app.schemas.trend_template import PlatformTrendTemplate


class SqlAlchemyTrendTemplateRepository:
    def __init__(self, session_factory: sessionmaker[Session] | None = None) -> None:
        self.session_factory = session_factory or get_session_factory()

    def list_templates(self, platform: str | None = None, content_type: str | None = None) -> list[PlatformTrendTemplate]:
        with self.session_factory() as session:
            statement = select(TrendTemplateModel).order_by(TrendTemplateModel.platform, TrendTemplateModel.content_type)
            if platform is not None:
                statement = statement.where(TrendTemplateModel.platform == platform)
            if content_type is not None:
                statement = statement.where(TrendTemplateModel.content_type == content_type)
            return [self._to_schema(item) for item in session.scalars(statement).all()]

    def save_templates(self, templates: list[PlatformTrendTemplate]) -> None:
        with self.session_factory() as session:
            for template in templates:
                self._upsert_template(session=session, template=template)
            session.commit()

    def get_best_match(self, platform: str, content_type: str) -> PlatformTrendTemplate | None:
        templates = self.list_templates()
        for item in templates:
            if item.platform == platform and item.content_type == content_type:
                return item
        for item in templates:
            if item.platform == platform and item.content_type == "auto":
                return item
        for item in templates:
            if item.platform == "bilibili" and item.content_type == "auto":
                return item
        return templates[0] if templates else None

    def count(self) -> int:
        with self.session_factory() as session:
            return len(session.scalars(select(TrendTemplateModel.id)).all())

    def _upsert_template(self, session: Session, template: PlatformTrendTemplate) -> None:
        statement = select(TrendTemplateModel).where(
            TrendTemplateModel.platform == template.platform,
            TrendTemplateModel.content_type == template.content_type,
        )
        existing = session.scalar(statement)
        payload = template.model_dump()
        if existing is None:
            session.add(TrendTemplateModel(**payload))
            return

        for key, value in payload.items():
            setattr(existing, key, value)

    def _to_schema(self, model: TrendTemplateModel) -> PlatformTrendTemplate:
        return PlatformTrendTemplate(
            platform=model.platform,
            content_type=model.content_type,
            summary=model.summary,
            hook_patterns=list(model.hook_patterns),
            rhythm_patterns=list(model.rhythm_patterns),
            title_cover_style=list(model.title_cover_style),
            audience_preference_summary=model.audience_preference_summary,
            avoid_patterns=list(model.avoid_patterns),
            hot_topics_summary=list(model.hot_topics_summary),
            interaction_patterns=list(model.interaction_patterns or []),
            emotional_entry_points=list(model.emotional_entry_points or []),
            creator_angle_summary=model.creator_angle_summary,
            source_trace=list(model.source_trace or []),
            source_type=model.source_type,
            updated_at=model.updated_at,
        )
