from __future__ import annotations

from datetime import UTC, datetime

from fastapi import HTTPException

from app.core.config import settings
from app.schemas.creation_request import CreationRequest
from app.schemas.profiles import AudienceProfile
from app.schemas.trend_template import (
    InternalTrendSummaryResponse,
    PlatformTrendTemplate,
    TrendRefreshResponse,
    TrendTemplateListResponse,
    TrendTemplateSummary,
)
from app.services.trend_collector.service import trend_collector_service
from app.services.trend_strategy.repository import TrendTemplateRepository


class TrendStrategyService:
    def __init__(self, repository: TrendTemplateRepository) -> None:
        self.repository = repository

    def _to_summary(self, template: PlatformTrendTemplate) -> TrendTemplateSummary:
        return TrendTemplateSummary(
            platform=template.platform,
            content_type=template.content_type,
            summary=template.summary,
            source_type=template.source_type,
            updated_at=template.updated_at,
            hook_patterns=template.hook_patterns,
            rhythm_patterns=template.rhythm_patterns,
            title_cover_style=template.title_cover_style,
            audience_preference_summary=template.audience_preference_summary,
            avoid_patterns=template.avoid_patterns,
            hot_topics_summary=template.hot_topics_summary,
            interaction_patterns=template.interaction_patterns,
            emotional_entry_points=template.emotional_entry_points,
            creator_angle_summary=template.creator_angle_summary,
            source_trace=template.source_trace,
            configured_sources=trend_collector_service.describe_platform_sources(template.platform),
        )

    def list_template_summaries(
        self,
        platform: str | None = None,
        content_type: str | None = None,
    ) -> TrendTemplateListResponse:
        templates = self.repository.list_templates(platform=platform, content_type=content_type)
        return TrendTemplateListResponse(
            items=[self._to_summary(item) for item in templates],
            total=len(templates),
            generated_at=datetime.now(UTC),
        )

    def get_platform_summary(
        self,
        platform: str,
        content_type: str | None = None,
    ) -> InternalTrendSummaryResponse:
        templates = self.repository.list_templates(platform=platform, content_type=content_type)
        if not templates:
            raise HTTPException(status_code=404, detail="Trend summary not found for platform")

        return InternalTrendSummaryResponse(
            platform=platform,
            items=[self._to_summary(item) for item in templates],
            total=len(templates),
            generated_at=datetime.now(UTC),
        )

    def refresh_templates(self) -> TrendRefreshResponse:
        refreshed_at = datetime.now(UTC)
        templates, source_type = trend_collector_service.refresh_templates(refreshed_at=refreshed_at)
        if source_type != "manual_refresh_fallback":
            self.repository.save_templates(templates)
            self.repository.write_seed_templates(templates)
        else:
            templates = self.repository.list_templates()
        return TrendRefreshResponse(
            refreshed_count=len(templates),
            source_type=source_type,
            updated_at=refreshed_at,
            items=[self._to_summary(item) for item in templates],
        )

    def get_template(self, request: CreationRequest, audience_profile: AudienceProfile) -> PlatformTrendTemplate:
        template = self.repository.get_best_match(
            platform=request.target_platform,
            content_type=request.content_type,
        )
        if template is None:
            raise HTTPException(status_code=500, detail="Trend template repository is empty")

        if "情绪共鸣" in audience_profile.interest_tags and "情绪议题" not in template.hot_topics_summary:
            template = template.model_copy(
                update={
                    "hot_topics_summary": [*template.hot_topics_summary, "情绪议题"],
                }
            )

        return template


trend_strategy_service = TrendStrategyService(
    repository=TrendTemplateRepository(settings.trend_templates_seed_path),
)
