from __future__ import annotations

from fastapi import HTTPException

from app.api.deps import require_internal_api_key
from app.api.routes.internal import get_platform_trend_summary, refresh_internal_trends
from app.core.config import settings
from app.schemas.trend_template import InternalTrendSummaryResponse, TrendRefreshResponse


def test_require_internal_api_key_rejects_missing_configuration(monkeypatch) -> None:
    monkeypatch.setattr(settings, "internal_api_key", None)

    try:
        require_internal_api_key("secret")
    except HTTPException as exc:
        assert exc.status_code == 503
    else:
        raise AssertionError("Expected missing internal API key configuration to raise")


def test_require_internal_api_key_rejects_invalid_key(monkeypatch) -> None:
    monkeypatch.setattr(settings, "internal_api_key", "expected-key")

    try:
        require_internal_api_key("wrong-key")
    except HTTPException as exc:
        assert exc.status_code == 403
    else:
        raise AssertionError("Expected invalid internal API key to raise")


def test_internal_trend_summary_route_uses_service(monkeypatch) -> None:
    expected = InternalTrendSummaryResponse.model_validate(
        {
            "platform": "bilibili",
            "items": [
                {
                    "platform": "bilibili",
                    "content_type": "science_popularization",
                    "summary": "平台偏好高信息密度和设问推进。",
                    "source_type": "db_truth",
                    "updated_at": "2026-03-27T00:00:00+00:00",
                    "hook_patterns": ["强设问开场", "高密度信息起手"],
                    "rhythm_patterns": ["先立问题", "再补推理链"],
                    "title_cover_style": ["设问式标题", "高密度封面"],
                    "audience_preference_summary": "观众偏好完整解释和世界观延展。",
                    "avoid_patterns": ["铺垫过长", "信息太散"],
                    "hot_topics_summary": ["时间悖论", "科幻设定拆解"],
                    "interaction_patterns": ["评论区补反例", "追问设定漏洞"],
                    "emotional_entry_points": ["认知冲突", "世界观好奇"],
                    "creator_angle_summary": "更适合从核心设问切入。",
                    "source_trace": [
                        {
                            "title": "时间悖论又上热榜了",
                            "link": "https://www.bilibili.com/video/BV1",
                            "excerpt": "近期热门内容更强调强设问开头。",
                            "source_name": "RSSHub / bilibili / /bilibili/popular/all",
                        }
                    ],
                    "configured_sources": [
                        {
                            "source_kind": "crawl_page",
                            "display_name": "Crawl4AI / bilibili_popular",
                            "target": "https://www.bilibili.com/v/popular/all",
                            "enabled": True,
                            "status": "active",
                            "rationale": "页面级抓取入口，在 feed 不足或未配置时继续作为稳定兜底来源。",
                        }
                    ],
                }
            ],
            "total": 1,
            "generated_at": "2026-03-27T00:00:00+00:00",
        }
    )
    monkeypatch.setattr(
        "app.api.routes.internal.trend_strategy_service.get_platform_summary",
        lambda platform, content_type=None: expected,
    )

    response = get_platform_trend_summary("bilibili")

    assert response == expected


def test_internal_trend_refresh_route_uses_service(monkeypatch) -> None:
    expected = TrendRefreshResponse.model_validate(
        {
            "refreshed_count": 1,
            "source_type": "manual_refresh_collected",
            "updated_at": "2026-03-27T00:00:00+00:00",
            "items": [
                {
                    "platform": "bilibili",
                    "content_type": "science_popularization",
                    "summary": "平台偏好高信息密度和设问推进。",
                    "source_type": "db_truth",
                    "updated_at": "2026-03-27T00:00:00+00:00",
                    "hook_patterns": ["强设问开场", "高密度信息起手"],
                    "rhythm_patterns": ["先立问题", "再补推理链"],
                    "title_cover_style": ["设问式标题", "高密度封面"],
                    "audience_preference_summary": "观众偏好完整解释和世界观延展。",
                    "avoid_patterns": ["铺垫过长", "信息太散"],
                    "hot_topics_summary": ["时间悖论", "科幻设定拆解"],
                    "interaction_patterns": ["评论区补反例", "追问设定漏洞"],
                    "emotional_entry_points": ["认知冲突", "世界观好奇"],
                    "creator_angle_summary": "更适合从核心设问切入。",
                    "source_trace": [
                        {
                            "title": "时间悖论又上热榜了",
                            "link": "https://www.bilibili.com/video/BV1",
                            "excerpt": "近期热门内容更强调强设问开头。",
                            "source_name": "RSSHub / bilibili / /bilibili/popular/all",
                        }
                    ],
                    "configured_sources": [
                        {
                            "source_kind": "crawl_page",
                            "display_name": "Crawl4AI / bilibili_popular",
                            "target": "https://www.bilibili.com/v/popular/all",
                            "enabled": True,
                            "status": "active",
                            "rationale": "页面级抓取入口，在 feed 不足或未配置时继续作为稳定兜底来源。",
                        }
                    ],
                }
            ],
        }
    )
    monkeypatch.setattr(
        "app.api.routes.internal.trend_strategy_service.refresh_templates",
        lambda: expected,
    )

    response = refresh_internal_trends()

    assert response == expected
