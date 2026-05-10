from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import logging
import os

from app.core.config import settings
from app.integrations.crawler.crawl4ai_adapter import Crawl4AIAdapter, Crawl4AIUnavailableError, CrawlDocument
from app.integrations.llm.aihubmix_search_adapter import (
    AIHubMixSearchAdapter,
    AIHubMixSearchRequest,
    AIHubMixSearchUnavailableError,
)
from app.integrations.rss.rsshub_adapter import RssHubAdapter, RssHubFeedItem, RssHubUnavailableError
from app.schemas.trend_template import (
    PlatformTrendTemplate,
    SearchBackedTrendObservation,
    StructuredTrendObservation,
    TrendConfiguredSource,
    TrendSourceTraceItem,
)
from app.services.structured_output_gateway.service import (
    StructuredOutputGatewayService,
    structured_output_gateway_service,
)
from app.services.trend_strategy.default_templates import build_refreshed_templates

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class TrendSource:
    platform: str
    content_type: str
    source_url: str
    source_name: str


@dataclass(slots=True)
class CollectedTrendDocument:
    document: CrawlDocument
    source_type: str
    source_trace: list[TrendSourceTraceItem]


DEFAULT_TREND_SOURCES: tuple[TrendSource, ...] = (
    TrendSource("douyin", "auto", "https://www.douyin.com/hot", "douyin_hot"),
    TrendSource("kuaishou", "auto", "https://www.kuaishou.com/hot", "kuaishou_hot"),
    TrendSource("xiaohongshu", "auto", "https://www.xiaohongshu.com/explore", "xiaohongshu_explore"),
    TrendSource("bilibili", "auto", "https://www.bilibili.com/v/popular/all", "bilibili_popular"),
    TrendSource("wechat_video", "auto", "https://channels.weixin.qq.com", "wechat_video_channels"),
)


class TrendCollectorService:
    min_markdown_length = 48

    def __init__(
        self,
        sources: tuple[TrendSource, ...] = DEFAULT_TREND_SOURCES,
        adapter_factory: type[Crawl4AIAdapter] = Crawl4AIAdapter,
        rsshub_adapter_factory: type[RssHubAdapter] = RssHubAdapter,
        structured_output_gateway: StructuredOutputGatewayService | None = None,
        rsshub_base_url: str | None = None,
        rsshub_platform_routes: dict[str, list[str] | str] | None = None,
        rsshub_item_limit: int = 5,
        search_adapter_factory: type[AIHubMixSearchAdapter] = AIHubMixSearchAdapter,
        aihubmix_api_key: str | None = None,
        aihubmix_base_url: str | None = None,
        aihubmix_search_model: str | None = None,
        aihubmix_timeout_seconds: float | None = None,
    ) -> None:
        self.sources = sources
        self.adapter_factory = adapter_factory
        self.rsshub_adapter_factory = rsshub_adapter_factory
        self.structured_output_gateway = structured_output_gateway or structured_output_gateway_service
        self.rsshub_base_url = rsshub_base_url
        self.rsshub_platform_routes = self._normalize_rsshub_routes(rsshub_platform_routes or {})
        self.rsshub_item_limit = rsshub_item_limit
        self.search_adapter_factory = search_adapter_factory
        self.aihubmix_api_key = aihubmix_api_key or settings.aihubmix_api_key or os.getenv("AIHUBMIX_API_KEY", "").strip() or None
        self.aihubmix_base_url = aihubmix_base_url or settings.aihubmix_base_url or os.getenv("AIHUBMIX_BASE_URL", "").strip() or None
        self.aihubmix_search_model = aihubmix_search_model or settings.aihubmix_search_model
        self.aihubmix_timeout_seconds = (
            settings.aihubmix_timeout_seconds if aihubmix_timeout_seconds is None else aihubmix_timeout_seconds
        )

    def refresh_templates(self, refreshed_at: datetime | None = None) -> tuple[list[PlatformTrendTemplate], str]:
        timestamp = refreshed_at or datetime.now(UTC)
        documents_by_platform = self._collect_documents()

        templates = self._build_templates_from_documents(documents_by_platform=documents_by_platform, refreshed_at=timestamp)
        if any(item.source_type == "aihubmix_search_collected" for item in templates):
            collected_source_type = "aihubmix_search_collected"
        elif not documents_by_platform:
            collected_source_type = "manual_refresh_fallback"
        elif any(item.source_type == "hybrid_collected" for item in documents_by_platform.values()):
            collected_source_type = "hybrid_collected"
        elif any(item.source_type == "rsshub_collected" for item in documents_by_platform.values()):
            collected_source_type = "rsshub_collected"
        else:
            collected_source_type = "manual_refresh_collected"
        return templates, collected_source_type

    def _collect_documents(self) -> dict[str, CollectedTrendDocument]:
        documents_by_platform = self._collect_rsshub_documents()

        try:
            adapter = self.adapter_factory()
        except Crawl4AIUnavailableError:
            return documents_by_platform

        for source in self.sources:
            try:
                document = self._fetch_document(adapter=adapter, source=source)
            except Crawl4AIUnavailableError:
                continue
            if not self._is_document_usable(document):
                continue
            collected_document = CollectedTrendDocument(
                document=document,
                source_type="manual_refresh_collected",
                source_trace=self._build_crawl_source_trace(source=source, document=document),
            )
            existing = documents_by_platform.get(source.platform)
            if existing is None:
                documents_by_platform[source.platform] = collected_document
                continue
            documents_by_platform[source.platform] = self._merge_collected_documents(existing, collected_document)

        return documents_by_platform

    def _collect_rsshub_documents(self) -> dict[str, CollectedTrendDocument]:
        if not self.rsshub_base_url or not self.rsshub_platform_routes:
            return {}

        try:
            adapter = self.rsshub_adapter_factory(
                base_url=self.rsshub_base_url,
                item_limit=self.rsshub_item_limit,
            )
        except RssHubUnavailableError:
            return {}

        documents_by_platform: dict[str, CollectedTrendDocument] = {}
        for platform, routes in self.rsshub_platform_routes.items():
            merged_document: CollectedTrendDocument | None = None
            for route in routes:
                try:
                    items = adapter.fetch_feed(route)
                except RssHubUnavailableError:
                    continue

                document = self._build_rsshub_document(platform=platform, route=route, items=items)
                if not self._is_document_usable(document):
                    continue
                candidate = CollectedTrendDocument(
                    document=document,
                    source_type="rsshub_collected",
                    source_trace=self._build_rsshub_source_trace(platform=platform, route=route, items=items),
                )
                merged_document = (
                    candidate
                    if merged_document is None
                    else self._merge_collected_documents(
                        merged_document,
                        candidate,
                        merged_source_type="rsshub_collected",
                    )
                )
            if merged_document is not None:
                documents_by_platform[platform] = merged_document

        return documents_by_platform

    def describe_platform_sources(self, platform: str) -> list[TrendConfiguredSource]:
        configured_sources: list[TrendConfiguredSource] = []
        rsshub_routes = self.rsshub_platform_routes.get(platform, ())
        for route in rsshub_routes:
            configured_sources.append(
                TrendConfiguredSource(
                    source_kind="rsshub_feed",
                    display_name=f"RSSHub / {platform}",
                    target=route,
                    enabled=bool(self.rsshub_base_url),
                    status="active" if self.rsshub_base_url else "awaiting_base_url",
                    rationale="成熟 feed 入口，用于把平台热点先收敛成可归纳的订阅流。",
                )
            )

        for source in self.sources:
            if source.platform != platform:
                continue
            configured_sources.append(
                TrendConfiguredSource(
                    source_kind="crawl_page",
                    display_name=f"Crawl4AI / {source.source_name}",
                    target=source.source_url,
                    enabled=True,
                    status="active",
                    rationale="页面级抓取入口，在 feed 不足或未配置时继续作为稳定兜底来源。",
                )
            )

        if platform == "bilibili":
            configured_sources.append(
                TrendConfiguredSource(
                    source_kind="research_candidate",
                    display_name="bilibili-api-python",
                    target="Nemo2011/bilibili-api",
                    enabled=False,
                    status="disabled_by_license",
                    rationale="GPL-3.0 许可证与当前主仓策略不兼容，保留研究价值，但正式退出主实现路径。",
                )
            )

        return configured_sources

    def _fetch_document(self, adapter: Crawl4AIAdapter, source: TrendSource) -> CrawlDocument:
        import asyncio

        return asyncio.run(adapter.fetch_document(source.source_url))

    def _build_templates_from_documents(
        self,
        documents_by_platform: dict[str, CollectedTrendDocument],
        refreshed_at: datetime,
    ) -> list[PlatformTrendTemplate]:
        templates = build_refreshed_templates(updated_at=refreshed_at)

        refreshed_templates: list[PlatformTrendTemplate] = []
        for template in templates:
            collected = documents_by_platform.get(template.platform)
            search_observation = self._build_search_observation(template=template, document=collected.document if collected else None)
            if search_observation is not None:
                refreshed_templates.append(
                    self._build_search_backed_template(
                        template=template,
                        observation=search_observation,
                        refreshed_at=refreshed_at,
                        native_source_trace=collected.source_trace if collected else [],
                    )
                )
                continue
            if collected is None:
                refreshed_templates.append(template)
                continue
            document = collected.document

            observation = self._build_structured_observation(template=template, document=document)
            if observation is not None:
                refreshed_templates.append(
                    template.model_copy(
                        update={
                            "summary": self._merge_summary(template.summary, observation.summary),
                            "hook_patterns": self._merge_list(observation.hook_patterns, template.hook_patterns),
                            "rhythm_patterns": self._merge_list(observation.rhythm_patterns, template.rhythm_patterns),
                            "title_cover_style": self._merge_list(
                                observation.title_cover_style,
                                template.title_cover_style,
                            ),
                            "audience_preference_summary": observation.audience_preference_summary.strip()
                            or template.audience_preference_summary,
                            "avoid_patterns": self._merge_list(observation.avoid_patterns, template.avoid_patterns),
                            "hot_topics_summary": self._merge_list(
                                [*observation.hot_topics_summary, f"来源:{document.title[:24]}"],
                                template.hot_topics_summary,
                                limit=5,
                            ),
                            "interaction_patterns": self._merge_list(
                                observation.interaction_patterns,
                                template.interaction_patterns,
                            ),
                            "emotional_entry_points": self._merge_list(
                                observation.emotional_entry_points,
                                template.emotional_entry_points,
                            ),
                            "creator_angle_summary": observation.creator_angle_summary.strip()
                            or template.creator_angle_summary,
                            "source_trace": collected.source_trace,
                            "source_type": collected.source_type,
                            "updated_at": refreshed_at,
                        }
                    )
                )
                continue

            refreshed_templates.append(
                self._build_excerpt_fallback_template(
                    template,
                    document,
                    refreshed_at,
                    collected.source_type,
                    collected.source_trace,
                )
            )
        return refreshed_templates

    def _build_search_observation(
        self,
        *,
        template: PlatformTrendTemplate,
        document: CrawlDocument | None,
    ) -> SearchBackedTrendObservation | None:
        try:
            adapter = self.search_adapter_factory(
                api_key=self.aihubmix_api_key or "",
                base_url=self.aihubmix_base_url or "",
                model=self.aihubmix_search_model or "",
                timeout_seconds=self.aihubmix_timeout_seconds,
            )
        except AIHubMixSearchUnavailableError:
            return None
        except TypeError:
            return None

        native_excerpt = self._compact_markdown(document.markdown)[:1600] if document else None
        try:
            return adapter.generate_observation(
                AIHubMixSearchRequest(
                    platform=template.platform,
                    content_type=template.content_type,
                    baseline_summary=template.summary,
                    baseline_hook_patterns=template.hook_patterns,
                    baseline_rhythm_patterns=template.rhythm_patterns,
                    baseline_title_cover_style=template.title_cover_style,
                    baseline_audience_preference_summary=template.audience_preference_summary,
                    baseline_avoid_patterns=template.avoid_patterns,
                    baseline_hot_topics_summary=template.hot_topics_summary,
                    baseline_interaction_patterns=template.interaction_patterns,
                    baseline_emotional_entry_points=template.emotional_entry_points,
                    baseline_creator_angle_summary=template.creator_angle_summary,
                    native_source_url=document.source_url if document else None,
                    native_source_title=document.title if document else None,
                    native_markdown_excerpt=native_excerpt,
                )
            )
        except Exception as exc:
            logger.warning(
                "trend_collector search fallback reason=aihubmix_search_failed platform=%s content_type=%s error=%s",
                template.platform,
                template.content_type,
                exc,
            )
            return None

    def _build_rsshub_document(
        self,
        *,
        platform: str,
        route: str,
        items: list[RssHubFeedItem],
    ) -> CrawlDocument:
        lines = [f"# RSSHub {platform} Trend Feed", ""]
        for index, item in enumerate(items, start=1):
            lines.extend(
                [
                    f"## {index}. {item.title}",
                    f"链接: {item.link}",
                    f"摘要: {item.description or '暂无摘要'}",
                    "",
                ]
            )

        return CrawlDocument(
            source_url=f"{self.rsshub_base_url.rstrip('/')}{route if route.startswith('/') else f'/{route}'}",
            title=f"RSSHub {platform} feed",
            markdown="\n".join(lines),
        )

    def _build_structured_observation(
        self,
        *,
        template: PlatformTrendTemplate,
        document: CrawlDocument,
    ) -> StructuredTrendObservation | None:
        return self.structured_output_gateway.generate(
            caller_name="trend_collector",
            response_model=StructuredTrendObservation,
            messages=self._build_structured_messages(template=template, document=document),
        )

    def _build_structured_messages(
        self,
        *,
        template: PlatformTrendTemplate,
        document: CrawlDocument,
    ) -> list[dict[str, str]]:
        compact_markdown = self._compact_markdown(document.markdown)[:2400]
        return [
            {
                "role": "system",
                "content": (
                    "你是平台趋势归纳器。"
                    "请根据当前平台模板基线和采集文档，输出可被 Pydantic StructuredTrendObservation 校验通过的结构化结果。"
                    "所有字段使用简短、具体、可复用的中文短语。"
                    "不要解释，不要输出 schema 之外的字段。"
                ),
            },
            {
                "role": "user",
                "content": (
                    f"平台: {template.platform}\n"
                    f"内容类型: {template.content_type}\n"
                    f"当前模板摘要: {template.summary}\n"
                    f"当前钩子模式: {', '.join(template.hook_patterns)}\n"
                    f"当前节奏模式: {', '.join(template.rhythm_patterns)}\n"
                    f"当前标题封面风格: {', '.join(template.title_cover_style)}\n"
                    f"当前受众偏好摘要: {template.audience_preference_summary}\n"
                    f"当前避免模式: {', '.join(template.avoid_patterns)}\n"
                    f"当前热点摘要: {', '.join(template.hot_topics_summary)}\n"
                    f"当前互动模式: {', '.join(template.interaction_patterns)}\n"
                    f"当前情绪切口: {', '.join(template.emotional_entry_points)}\n"
                    f"当前创作者角度摘要: {template.creator_angle_summary}\n"
                    f"采集来源标题: {document.title}\n"
                    f"采集来源 URL: {document.source_url}\n"
                    f"采集正文: {compact_markdown}\n"
                    "请基于采集正文归纳近期平台趋势，并尽量输出更像“近期新增观察”而不是机械重复旧模板。"
                ),
            },
        ]

    def _build_excerpt_fallback_template(
        self,
        template: PlatformTrendTemplate,
        document: CrawlDocument,
        refreshed_at: datetime,
        source_type: str,
        source_trace: list[TrendSourceTraceItem],
    ) -> PlatformTrendTemplate:
        excerpt = self._extract_excerpt(document.markdown)
        return template.model_copy(
            update={
                "summary": f"{template.summary} 采集摘要：{excerpt}",
                "hot_topics_summary": self._merge_list(
                    [f"来源:{document.title[:24]}"],
                    template.hot_topics_summary,
                    limit=5,
                ),
                "interaction_patterns": template.interaction_patterns,
                "emotional_entry_points": template.emotional_entry_points,
                "creator_angle_summary": template.creator_angle_summary,
                "source_trace": source_trace,
                "source_type": source_type,
                "updated_at": refreshed_at,
            }
        )

    def _build_search_backed_template(
        self,
        *,
        template: PlatformTrendTemplate,
        observation: SearchBackedTrendObservation,
        refreshed_at: datetime,
        native_source_trace: list[TrendSourceTraceItem],
    ) -> PlatformTrendTemplate:
        merged_source_trace: list[TrendSourceTraceItem] = []
        for item in [*native_source_trace, *observation.source_trace]:
            if any(existing.title == item.title and existing.source_name == item.source_name for existing in merged_source_trace):
                continue
            merged_source_trace.append(item)

        return template.model_copy(
            update={
                "summary": observation.summary.strip(),
                "hook_patterns": self._merge_list(observation.hook_patterns, template.hook_patterns),
                "rhythm_patterns": self._merge_list(observation.rhythm_patterns, template.rhythm_patterns),
                "title_cover_style": self._merge_list(observation.title_cover_style, template.title_cover_style),
                "audience_preference_summary": observation.audience_preference_summary.strip()
                or template.audience_preference_summary,
                "avoid_patterns": self._merge_list(observation.avoid_patterns, template.avoid_patterns),
                "hot_topics_summary": self._merge_list(observation.hot_topics_summary, template.hot_topics_summary, limit=5),
                "interaction_patterns": self._merge_list(observation.interaction_patterns, template.interaction_patterns),
                "emotional_entry_points": self._merge_list(
                    observation.emotional_entry_points,
                    template.emotional_entry_points,
                ),
                "creator_angle_summary": observation.creator_angle_summary.strip() or template.creator_angle_summary,
                "source_trace": merged_source_trace[:5],
                "source_type": "aihubmix_search_collected",
                "updated_at": refreshed_at,
            }
        )

    def _merge_collected_documents(
        self,
        primary: CollectedTrendDocument,
        secondary: CollectedTrendDocument,
        merged_source_type: str | None = None,
    ) -> CollectedTrendDocument:
        merged_markdown = "\n\n".join(
            [
                primary.document.markdown,
                "---",
                secondary.document.markdown,
            ]
        )
        merged_document = CrawlDocument(
            source_url=primary.document.source_url,
            title=f"{primary.document.title} + {secondary.document.title}",
            markdown=merged_markdown,
        )
        merged_trace: list[TrendSourceTraceItem] = []
        for item in [*primary.source_trace, *secondary.source_trace]:
            if any(existing.title == item.title and existing.source_name == item.source_name for existing in merged_trace):
                continue
            merged_trace.append(item)
        resolved_source_type = merged_source_type or (
            primary.source_type if primary.source_type == secondary.source_type else "hybrid_collected"
        )
        return CollectedTrendDocument(
            document=merged_document,
            source_type=resolved_source_type,
            source_trace=merged_trace[:5],
        )

    def _build_rsshub_source_trace(
        self,
        *,
        platform: str,
        route: str,
        items: list[RssHubFeedItem],
    ) -> list[TrendSourceTraceItem]:
        trace: list[TrendSourceTraceItem] = []
        for item in items[:3]:
            trace.append(
                TrendSourceTraceItem(
                    title=item.title.strip() or f"{platform} 趋势条目",
                    link=item.link,
                    excerpt=self._compact_excerpt(item.description or item.title),
                    source_name=f"RSSHub / {platform} / {route}",
                )
            )
        return trace

    def _normalize_rsshub_routes(
        self,
        raw_routes: dict[str, list[str] | str],
    ) -> dict[str, tuple[str, ...]]:
        normalized: dict[str, tuple[str, ...]] = {}
        for platform, value in raw_routes.items():
            routes = [value] if isinstance(value, str) else list(value)
            cleaned_routes = tuple(route.strip() for route in routes if route.strip())
            if cleaned_routes:
                normalized[platform] = cleaned_routes
        return normalized

    def _build_crawl_source_trace(
        self,
        *,
        source: TrendSource,
        document: CrawlDocument,
    ) -> list[TrendSourceTraceItem]:
        return [
            TrendSourceTraceItem(
                title=document.title.strip() or source.source_name,
                link=document.source_url,
                excerpt=self._extract_excerpt(document.markdown),
                source_name=f"Crawl4AI / {source.source_name}",
            )
        ]

    def _is_document_usable(self, document: CrawlDocument) -> bool:
        compact = self._compact_markdown(document.markdown)
        return len(compact) >= self.min_markdown_length

    def _extract_excerpt(self, markdown: str) -> str:
        compact = self._compact_markdown(markdown)
        return compact[:72] + ("..." if len(compact) > 72 else "")

    def _compact_excerpt(self, value: str, limit: int = 96) -> str:
        compact = " ".join(value.split())
        return compact[:limit] + ("..." if len(compact) > limit else "")

    def _merge_summary(self, base_summary: str, observation_summary: str) -> str:
        cleaned_observation = observation_summary.strip()
        if not cleaned_observation:
            return base_summary
        if cleaned_observation in base_summary:
            return base_summary
        return f"{base_summary} 近期归纳：{cleaned_observation}"

    def _merge_list(self, primary: list[str], fallback: list[str], limit: int = 4) -> list[str]:
        merged: list[str] = []
        for item in [*primary, *fallback]:
            normalized = item.strip()
            if not normalized or normalized in merged:
                continue
            merged.append(normalized)
            if len(merged) >= limit:
                break
        return merged

    def _compact_markdown(self, markdown: str) -> str:
        return " ".join(markdown.replace("#", " ").split())


trend_collector_service = TrendCollectorService(
    rsshub_base_url=settings.trend_rsshub_base_url,
    rsshub_platform_routes=settings.trend_rsshub_platform_routes,
    rsshub_item_limit=settings.trend_rsshub_item_limit,
)
