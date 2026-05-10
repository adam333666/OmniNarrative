from __future__ import annotations

import os
from datetime import UTC, datetime
from pathlib import Path

os.environ.setdefault("DATABASE_URL", f"sqlite+pysqlite:///{Path('/tmp/multi_media_test.db')}")

from app.integrations.crawler.crawl4ai_adapter import Crawl4AIUnavailableError, CrawlDocument
from app.integrations.llm.aihubmix_search_adapter import AIHubMixSearchAdapter, AIHubMixSearchRequest
from app.schemas.trend_template import SearchBackedTrendObservation, StructuredTrendObservation, TrendSourceTraceItem
from app.services.structured_output_gateway.service import StructuredOutputGatewayService
from app.services.trend_collector.service import TrendCollectorService, TrendSource


class MissingAdapter:
    def __init__(self) -> None:
        raise Crawl4AIUnavailableError("crawl4ai is unavailable")


class FakeAdapter:
    def __init__(self) -> None:
        pass

    async def fetch_document(self, source_url: str) -> CrawlDocument:
        return CrawlDocument(
            source_url=source_url,
            title="Native Trend Snapshot",
            markdown="# Hot Topic\n最近公开内容更强调强问题开头、具体案例展开、可继续讨论的观点和带反差的真实场景，用户更愿意在评论区继续补充自己的理解。",
        )


class FakeInstructorClient:
    def create(self, **_: object) -> StructuredTrendObservation:
        return StructuredTrendObservation(
            summary="近期更偏好先抛问题再给解释。",
            hook_patterns=["先抛问题", "先给结论"],
            rhythm_patterns=["前快后稳", "逐层解释"],
            title_cover_style=["问题式标题", "对比式封面"],
            audience_preference_summary="更喜欢容易理解又能继续讨论的表达。",
            avoid_patterns=["空话过多", "铺垫过长"],
            hot_topics_summary=["社会情绪", "知识拆解"],
            interaction_patterns=["评论区补案例", "追问细节"],
            emotional_entry_points=["认知冲突", "焦虑共鸣"],
            creator_angle_summary="适合从问题切入，再给具体解释。",
        )


class FakeSearchAdapter:
    def __init__(self, **_: object) -> None:
        pass

    def generate_observation(self, request) -> SearchBackedTrendObservation:
        return SearchBackedTrendObservation(
            summary=f"{request.platform}-{request.content_type} 近期更偏好强问题开头、真实案例和可转述结论。",
            hook_patterns=["先抛真实问题", "先给强对比判断"],
            rhythm_patterns=["开头快", "中段补案例"],
            title_cover_style=["问题式标题", "结论先行封面"],
            audience_preference_summary="更喜欢能立刻看懂、又能继续讨论的内容。",
            avoid_patterns=["空洞总结", "结尾无落点"],
            hot_topics_summary=["平台热议议题", "真实案例"],
            interaction_patterns=["评论区接龙举例", "收藏后回看结论"],
            emotional_entry_points=["共鸣焦虑", "认知反差"],
            creator_angle_summary="更适合先给问题，再给案例和判断。",
            source_trace=[
                TrendSourceTraceItem(
                    title=f"{request.platform} trend 1",
                    link="https://example.com/1",
                    excerpt="来源一摘要",
                    source_name="aihubmix_search",
                ),
                TrendSourceTraceItem(
                    title=f"{request.platform} trend 2",
                    link="https://example.com/2",
                    excerpt="来源二摘要",
                    source_name="aihubmix_search",
                ),
            ],
        )


def test_aihubmix_search_adapter_normalizes_sparse_combined_fields() -> None:
    adapter = AIHubMixSearchAdapter(
        api_key="test-key",
        base_url="https://example.com/v1",
        model="gemini-3.1-flash-lite-preview",
    )
    request = AIHubMixSearchRequest(
        platform="bilibili",
        content_type="science_popularization",
        baseline_summary="基线摘要",
        baseline_hook_patterns=["先抛核心问题", "先给反常识结论"],
        baseline_rhythm_patterns=["前段快提问", "中段补解释链"],
        baseline_title_cover_style=["问题拆解式标题", "结论先行封面文案"],
        baseline_audience_preference_summary="基线受众偏好",
        baseline_avoid_patterns=["术语堆叠过多", "解释链断裂"],
        baseline_hot_topics_summary=["知识拆解", "反常识问题"],
        baseline_interaction_patterns=["评论区追问原理", "补充反例和案例"],
        baseline_emotional_entry_points=["认知冲突", "求知欲"],
        baseline_creator_angle_summary="基线创作者角度",
    )

    normalized = adapter._normalize_payload(
        {
            "summary": ["近期更适合先提问题", "再给解释链"],
            "hook_patterns": "先抛核心问题、先给反常识结论",
            "rhythm_patterns": ["前段快提问，中段补解释链"],
            "title_cover_style": "问题拆解式标题",
            "audience_preference_summary": ["偏好快速看懂", "也要能继续讨论"],
            "avoid_patterns": ["术语堆叠过多"],
            "hot_topics_summary": ["知识拆解、反常识问题"],
            "interaction_patterns": "评论区追问原理",
            "emotional_entry_points": ["认知冲突"],
            "creator_angle_summary": ["先给判断", "再给案例"],
            "source_trace": [
                {
                    "title": "trend 1",
                    "link": "https://example.com/1",
                    "excerpt": "来源一",
                    "source_name": "aihubmix_search",
                },
                {
                    "title": "trend 2",
                    "link": "https://example.com/2",
                    "excerpt": "来源二",
                    "source_name": "aihubmix_search",
                },
            ],
        },
        request,
    )

    observation = SearchBackedTrendObservation.model_validate(normalized)

    assert observation.summary == "近期更适合先提问题；再给解释链"
    assert observation.hook_patterns == ["先抛核心问题", "先给反常识结论"]
    assert observation.rhythm_patterns == ["前段快提问", "中段补解释链"]
    assert observation.title_cover_style == ["问题拆解式标题", "结论先行封面文案"]
    assert observation.avoid_patterns == ["术语堆叠过多", "解释链断裂"]
    assert observation.hot_topics_summary == ["知识拆解", "反常识问题"]
    assert observation.interaction_patterns == ["评论区追问原理", "补充反例和案例"]
    assert observation.emotional_entry_points == ["认知冲突", "求知欲"]
    assert observation.creator_angle_summary == "先给判断；再给案例"


def test_trend_collector_generates_search_backed_variants_without_native_documents() -> None:
    service = TrendCollectorService(
        adapter_factory=MissingAdapter,
        structured_output_gateway=StructuredOutputGatewayService(
            instructor_client_factory=FakeInstructorClient,
            provider_name="litellm",
            model_name="openai/gpt-4o-mini",
        ),
        search_adapter_factory=FakeSearchAdapter,
        aihubmix_api_key="test-key",
        aihubmix_base_url="https://example.com/v1",
        aihubmix_search_model="openai/gpt-4o-mini-search-preview",
    )

    templates, source_type = service.refresh_templates(refreshed_at=datetime(2026, 4, 2, tzinfo=UTC))

    assert source_type == "aihubmix_search_collected"
    selected = [item for item in templates if item.platform == "bilibili" and item.content_type in {"auto", "science_popularization", "story"}]
    assert len(selected) == 3
    assert all(item.source_type == "aihubmix_search_collected" for item in selected)
    assert all(len(item.source_trace) == 2 for item in selected)


def test_trend_collector_merges_native_and_search_sources() -> None:
    service = TrendCollectorService(
        sources=(TrendSource("bilibili", "auto", "https://www.bilibili.com/v/popular/all", "bilibili_popular"),),
        adapter_factory=FakeAdapter,
        structured_output_gateway=StructuredOutputGatewayService(
            instructor_client_factory=FakeInstructorClient,
            provider_name="litellm",
            model_name="openai/gpt-4o-mini",
        ),
        search_adapter_factory=FakeSearchAdapter,
        aihubmix_api_key="test-key",
        aihubmix_base_url="https://example.com/v1",
        aihubmix_search_model="openai/gpt-4o-mini-search-preview",
    )

    templates, source_type = service.refresh_templates(refreshed_at=datetime(2026, 4, 2, tzinfo=UTC))

    assert source_type == "aihubmix_search_collected"
    bilibili_auto = next(item for item in templates if item.platform == "bilibili" and item.content_type == "auto")
    assert bilibili_auto.source_type == "aihubmix_search_collected"
    assert any(trace.source_name == "aihubmix_search" for trace in bilibili_auto.source_trace)
    assert any(trace.source_name == "Crawl4AI / bilibili_popular" for trace in bilibili_auto.source_trace)
