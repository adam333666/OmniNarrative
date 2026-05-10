from datetime import datetime

from pydantic import BaseModel, Field


class TrendSourceTraceItem(BaseModel):
    title: str
    link: str | None = None
    excerpt: str
    source_name: str


class TrendConfiguredSource(BaseModel):
    source_kind: str
    display_name: str
    target: str
    enabled: bool = True
    status: str = "active"
    rationale: str = ""


class PlatformTrendTemplate(BaseModel):
    platform: str
    content_type: str = "auto"
    summary: str
    hook_patterns: list[str]
    rhythm_patterns: list[str]
    title_cover_style: list[str]
    audience_preference_summary: str
    avoid_patterns: list[str]
    hot_topics_summary: list[str]
    interaction_patterns: list[str] = Field(default_factory=list)
    emotional_entry_points: list[str] = Field(default_factory=list)
    creator_angle_summary: str = ""
    source_trace: list[TrendSourceTraceItem] = Field(default_factory=list)
    source_type: str = "seed"
    updated_at: datetime | None = None


class StructuredTrendObservation(BaseModel):
    summary: str = Field(description="对当前平台近期内容趋势的结构化摘要。")
    hook_patterns: list[str] = Field(min_length=2, max_length=4, description="近期有效的开场钩子模式。")
    rhythm_patterns: list[str] = Field(min_length=2, max_length=4, description="近期有效的内容节奏模式。")
    title_cover_style: list[str] = Field(min_length=2, max_length=4, description="近期更常见的标题或封面表达方式。")
    audience_preference_summary: str = Field(description="近期该平台受众偏好的归纳。")
    avoid_patterns: list[str] = Field(min_length=2, max_length=4, description="近期需要规避的表达模式。")
    hot_topics_summary: list[str] = Field(min_length=2, max_length=5, description="近期反复出现的高热话题或讨论点。")
    interaction_patterns: list[str] = Field(min_length=2, max_length=4, description="近期更有效的互动触发方式。")
    emotional_entry_points: list[str] = Field(min_length=2, max_length=4, description="近期更有效的情绪切入点。")
    creator_angle_summary: str = Field(description="近期更适合创作者采用的表达角度摘要。")


class SearchBackedTrendObservation(StructuredTrendObservation):
    source_trace: list[TrendSourceTraceItem] = Field(min_length=2, max_length=4)


class TrendTemplateSummary(BaseModel):
    platform: str
    content_type: str
    summary: str
    source_type: str
    updated_at: datetime | None
    hook_patterns: list[str]
    rhythm_patterns: list[str]
    title_cover_style: list[str]
    audience_preference_summary: str
    avoid_patterns: list[str]
    hot_topics_summary: list[str]
    interaction_patterns: list[str] = Field(default_factory=list)
    emotional_entry_points: list[str] = Field(default_factory=list)
    creator_angle_summary: str = ""
    source_trace: list[TrendSourceTraceItem] = Field(default_factory=list)
    configured_sources: list[TrendConfiguredSource] = Field(default_factory=list)


class TrendTemplateListResponse(BaseModel):
    items: list[TrendTemplateSummary]
    total: int
    generated_at: datetime


class InternalTrendSummaryResponse(BaseModel):
    platform: str
    items: list[TrendTemplateSummary]
    total: int
    generated_at: datetime


class TrendRefreshResponse(BaseModel):
    refreshed_count: int
    source_type: str
    updated_at: datetime
    items: list[TrendTemplateSummary]
