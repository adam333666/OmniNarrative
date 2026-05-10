from __future__ import annotations

import os
from datetime import UTC, datetime
from pathlib import Path

os.environ.setdefault("DATABASE_URL", f"sqlite+pysqlite:///{Path('/tmp/multi_media_test.db')}")

from app.integrations.crawler.crawl4ai_adapter import Crawl4AIUnavailableError
from app.integrations.rss.rsshub_adapter import RssHubFeedItem, RssHubUnavailableError
from app.schemas.trend_template import StructuredTrendObservation
from app.services.structured_output_gateway.service import StructuredOutputGatewayService
from app.services.trend_collector.service import TrendCollectorService, TrendSource


class MissingAdapter:
    def __init__(self) -> None:
        raise Crawl4AIUnavailableError("crawl4ai is unavailable")


class FakeCrawlAdapter:
    async def fetch_document(self, source_url: str):
        from app.integrations.crawler.crawl4ai_adapter import CrawlDocument

        return CrawlDocument(
            source_url=source_url,
            title="Bilibili popular page",
            markdown=(
                "热门页面里高频出现设问推进、长解释链和评论区补反例的表达，"
                "同时经常围绕世界观漏洞继续追问，并把反例讨论拉长成完整推理链。"
            ),
        )


class FakeRssHubAdapter:
    def __init__(self, *, base_url: str, item_limit: int = 5) -> None:
        self.base_url = base_url
        self.item_limit = item_limit

    def fetch_feed(self, route: str) -> list[RssHubFeedItem]:
        if route != "/bilibili/popular/all":
            raise RssHubUnavailableError("route not found")

        return [
            RssHubFeedItem(
                title="时间悖论又上热榜了",
                link="https://www.bilibili.com/video/BV1",
                description="近期热门内容更强调强设问开头、完整解释链和评论区补充世界观。",
            ),
            RssHubFeedItem(
                title="为什么观众更愿意看完整推理链",
                link="https://www.bilibili.com/video/BV2",
                description="用户更偏好信息密度高、能引发评论区补充和反例讨论的知识内容。",
            ),
        ]


class FakeInstructorClient:
    def create(self, **_: object) -> StructuredTrendObservation:
        return StructuredTrendObservation(
            summary="近期更强调强设问起手、完整解释链和评论区延展讨论。",
            hook_patterns=["先抛核心矛盾", "先给强设问结论"],
            rhythm_patterns=["前段快速起势", "中段完整解释"],
            title_cover_style=["高信息密度标题", "设问式封面"],
            audience_preference_summary="用户偏好快速进入问题，同时保留完整推理过程。",
            avoid_patterns=["铺垫过长", "没有反例支撑"],
            hot_topics_summary=["世界观讨论", "完整推理链", "评论区补充"],
            interaction_patterns=["评论区补反例", "结尾追问设定漏洞"],
            emotional_entry_points=["认知冲突", "世界观好奇"],
            creator_angle_summary="更适合从核心设问和世界观冲突切入。",
        )


def test_trend_collector_uses_rsshub_feed_when_configured(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    service = TrendCollectorService(
        adapter_factory=MissingAdapter,
        rsshub_adapter_factory=FakeRssHubAdapter,
        rsshub_base_url="https://rsshub.example",
        rsshub_platform_routes={"bilibili": "/bilibili/popular/all"},
        structured_output_gateway=StructuredOutputGatewayService(
            instructor_client_factory=FakeInstructorClient,
            provider_name="litellm",
            model_name="openai/gpt-4o-mini",
        ),
    )

    templates, source_type = service.refresh_templates(refreshed_at=datetime(2026, 3, 27, tzinfo=UTC))

    assert source_type == "rsshub_collected"
    bilibili = next(item for item in templates if item.platform == "bilibili")
    assert "近期归纳" in bilibili.summary
    assert bilibili.source_type == "rsshub_collected"
    assert bilibili.hook_patterns[0] == "先抛核心矛盾"
    assert "世界观讨论" in bilibili.hot_topics_summary
    assert len(bilibili.source_trace) == 2
    assert bilibili.source_trace[0].source_name == "RSSHub / bilibili / /bilibili/popular/all"
    assert bilibili.source_trace[0].link == "https://www.bilibili.com/video/BV1"
    assert bilibili.interaction_patterns[0] == "评论区补反例"
    assert bilibili.creator_angle_summary.startswith("更适合从核心设问")


def test_trend_collector_merges_rsshub_and_crawl_sources_for_same_platform(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    service = TrendCollectorService(
        sources=(
            TrendSource(
                "bilibili",
                "auto",
                "https://www.bilibili.com/v/popular/all",
                "bilibili_popular",
            ),
        ),
        adapter_factory=FakeCrawlAdapter,
        rsshub_adapter_factory=FakeRssHubAdapter,
        rsshub_base_url="https://rsshub.example",
        rsshub_platform_routes={"bilibili": "/bilibili/popular/all"},
        structured_output_gateway=StructuredOutputGatewayService(
            instructor_client_factory=FakeInstructorClient,
            provider_name="litellm",
            model_name="openai/gpt-4o-mini",
        ),
    )

    templates, source_type = service.refresh_templates(refreshed_at=datetime(2026, 3, 30, tzinfo=UTC))

    assert source_type == "hybrid_collected"
    bilibili = next(item for item in templates if item.platform == "bilibili")
    assert bilibili.source_type == "hybrid_collected"
    assert len(bilibili.source_trace) >= 2
    assert any(item.source_name.startswith("RSSHub") for item in bilibili.source_trace)
    assert any(item.source_name.startswith("Crawl4AI") for item in bilibili.source_trace)
