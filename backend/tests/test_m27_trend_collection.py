from __future__ import annotations

import os
from datetime import UTC, datetime
from pathlib import Path

os.environ.setdefault("DATABASE_URL", f"sqlite+pysqlite:///{Path('/tmp/multi_media_test.db')}")

from app.integrations.crawler.crawl4ai_adapter import Crawl4AIUnavailableError, CrawlDocument
from app.schemas.trend_template import StructuredTrendObservation
from app.services.trend_collector.service import TrendCollectorService, TrendSource
from app.services.structured_output_gateway.service import StructuredOutputGatewayService


class FakeAdapter:
    def __init__(self) -> None:
        pass

    async def fetch_document(self, source_url: str) -> CrawlDocument:
        return CrawlDocument(
            source_url=source_url,
            title="Platform Trend Snapshot",
            markdown="# Hot Topic\n短视频平台近期更强调反常识开头、情绪推进与结构化解释，用户会继续追问细节和反例，适合做持续延展的话题内容。",
        )


class MissingAdapter:
    def __init__(self) -> None:
        raise Crawl4AIUnavailableError("crawl4ai is unavailable")


class MixedQualityAdapter:
    def __init__(self) -> None:
        pass

    async def fetch_document(self, source_url: str) -> CrawlDocument:
        if "bilibili" in source_url:
            return CrawlDocument(
                source_url=source_url,
                title="Bilibili Trend Snapshot",
                markdown="# Hot Topic\nB站近期热门内容更强调强设问开场、知识密度与完整解释链条，评论区偏好补充世界观与反例讨论。",
            )
        if "xiaohongshu" in source_url:
            return CrawlDocument(
                source_url=source_url,
                title="Too Short",
                markdown="太短了",
            )
        raise Crawl4AIUnavailableError("source not reachable")


class FakeInstructorClient:
    def create(self, **_: object) -> StructuredTrendObservation:
        return StructuredTrendObservation(
            summary="近期更强调反常识设问开场、信息递进和可复述结论。",
            hook_patterns=["先抛反常识问题", "先给强设问结论"],
            rhythm_patterns=["前段快速起势", "中段递进解释"],
            title_cover_style=["设问式标题", "强对比封面文案"],
            audience_preference_summary="更偏好能快速进入核心、同时保留解释完整度的表达。",
            avoid_patterns=["空泛抒情", "重复旧梗"],
            hot_topics_summary=["反常识知识点", "完整解释链"],
            interaction_patterns=["评论区补案例", "转发时强调结论"],
            emotional_entry_points=["认知冲击", "问题焦虑"],
            creator_angle_summary="更适合从反常识问题和解释链切入。",
        )


class BrokenInstructorClient:
    def create(self, **_: object) -> StructuredTrendObservation:
        raise RuntimeError("structured extraction failed")


class MultiRouteRssAdapter:
    def __init__(self, *, base_url: str, item_limit: int = 5) -> None:
        self.base_url = base_url
        self.item_limit = item_limit

    def fetch_feed(self, route: str):
        route_payloads = {
            "/bilibili/popular/all": [
                {
                    "title": "热门总榜强调强设问开头",
                    "link": "https://www.bilibili.com/video/BV100",
                    "description": "热门总榜里更强调强设问起手和知识密度。",
                }
            ],
            "/bilibili/knowledge": [
                {
                    "title": "知识区持续拉长解释链",
                    "link": "https://www.bilibili.com/video/BV101",
                    "description": "知识区内容更强调完整推理链和评论区补反例。",
                }
            ],
        }
        if route not in route_payloads:
            raise Crawl4AIUnavailableError("route not reachable")
        from app.integrations.rss.rsshub_adapter import RssHubFeedItem

        return [RssHubFeedItem(**item) for item in route_payloads[route]]


def test_trend_collector_uses_fake_adapter_when_available() -> None:
    service = TrendCollectorService(
        sources=(TrendSource("bilibili", "auto", "https://example.com", "fixture"),),
        adapter_factory=FakeAdapter,
        structured_output_gateway=StructuredOutputGatewayService(
            instructor_client_factory=FakeInstructorClient,
            provider_name="litellm",
            model_name="openai/gpt-4o-mini",
        ),
    )

    templates, source_type = service.refresh_templates(refreshed_at=datetime(2026, 3, 25, tzinfo=UTC))

    assert source_type == "manual_refresh_collected"
    template = next(item for item in templates if item.platform == "bilibili")
    assert "近期归纳" in template.summary
    assert template.hook_patterns[0] == "先抛反常识问题"
    assert template.rhythm_patterns[0] == "前段快速起势"
    assert template.title_cover_style[0] == "设问式标题"
    assert template.audience_preference_summary.startswith("更偏好能快速进入核心")
    assert "反常识知识点" in template.hot_topics_summary
    assert template.source_type == "manual_refresh_collected"


def test_trend_collector_falls_back_when_adapter_is_unavailable() -> None:
    service = TrendCollectorService(adapter_factory=MissingAdapter)

    templates, source_type = service.refresh_templates(refreshed_at=datetime(2026, 3, 25, tzinfo=UTC))

    assert source_type == "manual_refresh_fallback"
    assert len(templates) >= 5
    assert all(item.source_type == "manual_refresh" for item in templates)


def test_trend_collector_keeps_partial_quality_results_without_global_fallback() -> None:
    service = TrendCollectorService(
        sources=(
            TrendSource("bilibili", "auto", "https://www.bilibili.com/v/popular/all", "bilibili_popular"),
            TrendSource("xiaohongshu", "auto", "https://www.xiaohongshu.com/explore", "xiaohongshu_explore"),
            TrendSource("douyin", "auto", "https://www.douyin.com/hot", "douyin_hot"),
        ),
        adapter_factory=MixedQualityAdapter,
        structured_output_gateway=StructuredOutputGatewayService(
            instructor_client_factory=FakeInstructorClient,
            provider_name="litellm",
            model_name="openai/gpt-4o-mini",
        ),
    )

    templates, source_type = service.refresh_templates(refreshed_at=datetime(2026, 3, 25, tzinfo=UTC))

    assert source_type == "manual_refresh_collected"
    bilibili = next(item for item in templates if item.platform == "bilibili")
    xiaohongshu = next(item for item in templates if item.platform == "xiaohongshu")
    assert "近期归纳" in bilibili.summary
    assert bilibili.source_type == "manual_refresh_collected"
    assert "采集摘要" not in xiaohongshu.summary
    assert xiaohongshu.source_type == "manual_refresh"


def test_trend_collector_falls_back_to_excerpt_when_structured_extraction_fails() -> None:
    service = TrendCollectorService(
        sources=(TrendSource("bilibili", "auto", "https://example.com", "fixture"),),
        adapter_factory=FakeAdapter,
        structured_output_gateway=StructuredOutputGatewayService(
            instructor_client_factory=BrokenInstructorClient,
            provider_name="litellm",
            model_name="openai/gpt-4o-mini",
        ),
    )

    templates, source_type = service.refresh_templates(refreshed_at=datetime(2026, 3, 25, tzinfo=UTC))

    assert source_type == "manual_refresh_collected"
    template = next(item for item in templates if item.platform == "bilibili")
    assert "采集摘要" in template.summary
    assert "近期归纳" not in template.summary
    assert template.source_type == "manual_refresh_collected"


def test_trend_collector_merges_multiple_rsshub_routes_for_same_platform() -> None:
    service = TrendCollectorService(
        adapter_factory=MissingAdapter,
        rsshub_adapter_factory=MultiRouteRssAdapter,
        rsshub_base_url="https://rsshub.example",
        rsshub_platform_routes={
            "bilibili": ["/bilibili/popular/all", "/bilibili/knowledge"],
        },
        structured_output_gateway=StructuredOutputGatewayService(
            instructor_client_factory=FakeInstructorClient,
            provider_name="litellm",
            model_name="openai/gpt-4o-mini",
        ),
    )

    templates, source_type = service.refresh_templates(refreshed_at=datetime(2026, 3, 30, tzinfo=UTC))

    assert source_type == "rsshub_collected"
    bilibili = next(item for item in templates if item.platform == "bilibili")
    assert bilibili.source_type == "rsshub_collected"
    assert len(bilibili.source_trace) == 2
    assert "RSSHub / bilibili / /bilibili/popular/all" in {item.source_name for item in bilibili.source_trace}
    assert "RSSHub / bilibili / /bilibili/knowledge" in {item.source_name for item in bilibili.source_trace}
