from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("DATABASE_URL", f"sqlite+pysqlite:///{Path('/tmp/multi_media_test.db')}")

from app.schemas.creation_request import CreationRequest
from app.schemas.narrative_generation import StructuredNarrativeBundle
from app.schemas.narrative_package import KeyShot, ScriptSegment
from app.schemas.profiles import AudienceProfile, StyleProfile
from app.schemas.trend_template import PlatformTrendTemplate
from app.services.narrative_generator.service import NarrativeGeneratorService
from app.services.structured_output_gateway.service import StructuredOutputGatewayService


class FakeInstructorClient:
    def __init__(self, bundle: StructuredNarrativeBundle) -> None:
        self.bundle = bundle
        self.calls: list[dict] = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return self.bundle


REQUEST = CreationRequest(
    theme_text="时间旅行悖论",
    content_type="science_popularization",
    target_platform="bilibili",
    target_audience_text="18到28岁，喜欢科幻设定和逻辑推理的观众",
    style_tone="suspense",
    custom_style_text="保持一点烧脑感",
)

AUDIENCE = AudienceProfile(
    raw_text="喜欢科幻设定和逻辑推理的年轻观众",
    age_group_guess="18-28岁",
    interest_tags=["科幻", "逻辑推理"],
    pain_points=["担心听不懂"],
    content_preference=["完整解释"],
    emotion_preference=["悬疑推进"],
)

STYLE = StyleProfile(
    style_label="悬疑",
    emotion_label="悬疑且有解释欲",
    intensity_level="medium",
    custom_notes="保持一点烧脑感",
)

TREND = PlatformTrendTemplate(
    platform="bilibili",
    content_type="auto",
    summary="设问推进、知识密度和完整解释链条。",
    hook_patterns=["先抛核心设问", "先给世界观矛盾"],
    rhythm_patterns=["完整铺垫", "中段密度提升"],
    title_cover_style=["命题式标题"],
    audience_preference_summary="接受解释、推理和结构化展开。",
    avoid_patterns=["只给结论不给推理"],
    hot_topics_summary=["设定讨论"],
    source_type="manual_refresh_collected",
)


def test_model_first_narrative_prefers_structured_bundle() -> None:
    bundle = StructuredNarrativeBundle(
        main_title="时间旅行悖论，第一秒就把人钩进去的讲法",
        one_sentence_summary="用悬疑推进和完整解释链条，把复杂设定讲得既好懂又上头。",
        segments=[
            ScriptSegment(
                segment_number=1,
                segment_title="反常识开场",
                segment_goal="第一秒抓住注意力",
                narration="先抛一个会让人停住的问题。",
                subtitle_text="你以为理解了，其实刚刚开始。",
                visual_description="高对比问题字幕叠加概念画面。",
                emotion="悬疑且有解释欲",
                rhythm="完整铺垫",
            ),
            ScriptSegment(
                segment_number=2,
                segment_title="拆解悖论",
                segment_goal="把复杂设定讲清楚",
                narration="从两个切面拆开这个悖论。",
                subtitle_text="真正难的不是答案，是转弯那一下。",
                visual_description="图示与人物反应交替。",
                emotion="悬疑且有解释欲",
                rhythm="中段密度提升",
            ),
            ScriptSegment(
                segment_number=3,
                segment_title="结尾余味",
                segment_goal="留下讨论空间",
                narration="把结尾收束成可评论的判断。",
                subtitle_text="你会记住的，是那一步转弯。",
                visual_description="镜头放慢，最后一句停住。",
                emotion="悬疑且有解释欲",
                rhythm="收束停顿",
            ),
        ],
        key_shots=[
            KeyShot(
                shot_title="问题镜头",
                shot_focus="第一句设问",
                shot_duration_seconds=4,
                transition_hint="直接切入",
            ),
            KeyShot(
                shot_title="解释镜头",
                shot_focus="悖论拆解",
                shot_duration_seconds=6,
                transition_hint="从问题转解释",
            ),
        ],
        title_alternatives=["时间旅行悖论，你可能一直都想简单了", "把悖论讲上头，其实就差这一步"],
        hook_alternatives=["如果结果会先于原因出现，你还敢相信时间吗？", "这不是科幻设定，它像极了你熟悉的困惑。"],
    )
    client = FakeInstructorClient(bundle)
    service = NarrativeGeneratorService(
        structured_output_gateway=StructuredOutputGatewayService(
            instructor_client_factory=lambda: client,
            provider_name="litellm",
            model_name="openai/gpt-4o-mini",
            max_retries=2,
            temperature=0.2,
        ),
    )

    result = service.build_narrative_bundle_result(
        REQUEST,
        AUDIENCE,
        STYLE,
        TREND,
    )

    assert result.title == bundle.main_title
    assert result.one_sentence_summary == bundle.one_sentence_summary
    assert result.segments == bundle.segments
    assert result.key_shots == bundle.key_shots
    assert len(result.title_alternatives) == 3
    assert len(result.hook_alternatives) == 3
    assert result.runtime.source_type == "structured_output_gateway"
    assert result.runtime.fallback_reason is None
    assert client.calls[0]["response_model"] is StructuredNarrativeBundle
    assert client.calls[0]["model"] == "openai/gpt-4o-mini"


def test_model_first_narrative_falls_back_to_template_bundle() -> None:
    service = NarrativeGeneratorService(
        structured_output_gateway=StructuredOutputGatewayService(
            instructor_client_factory=lambda: (_ for _ in ()).throw(RuntimeError("instructor unavailable")),
            provider_name="litellm",
            model_name="openai/gpt-4o-mini",
        ),
    )

    result = service.build_narrative_bundle_result(
        REQUEST,
        AUDIENCE,
        STYLE,
        TREND,
    )

    assert result.title == service.build_main_title(REQUEST, TREND)
    assert result.one_sentence_summary == service.build_one_sentence_summary(REQUEST, AUDIENCE, STYLE)
    assert len(result.segments) == 4
    assert len(result.key_shots) == 3
    assert len(result.title_alternatives) == 3
    assert len(result.hook_alternatives) == 3
    assert result.runtime.source_type == "narrative_generator_fallback"
    assert result.runtime.fallback_reason == "structured_output_unavailable_or_failed"


def test_model_first_narrative_fallback_tolerates_sparse_profiles_and_trends() -> None:
    service = NarrativeGeneratorService(
        structured_output_gateway=StructuredOutputGatewayService(
            instructor_client_factory=lambda: (_ for _ in ()).throw(RuntimeError("instructor unavailable")),
            provider_name="litellm",
            model_name="openai/gpt-4o-mini",
        ),
    )

    sparse_audience = AudienceProfile(
        raw_text="喜欢科幻设定和逻辑推理的年轻观众",
        age_group_guess="18-28岁",
        interest_tags=[],
        pain_points=["担心听不懂"],
        content_preference=["完整解释"],
        emotion_preference=["悬疑推进"],
    )
    sparse_trend = PlatformTrendTemplate(
        platform="bilibili",
        content_type="auto",
        summary="设问推进、知识密度和完整解释链条。",
        hook_patterns=[],
        rhythm_patterns=[],
        title_cover_style=["命题式标题"],
        audience_preference_summary="接受解释、推理和结构化展开。",
        avoid_patterns=[],
        hot_topics_summary=["设定讨论"],
        source_type="manual_refresh_collected",
    )

    result = service.build_narrative_bundle_result(
        REQUEST,
        sparse_audience,
        STYLE,
        sparse_trend,
    )

    assert result.segments[0].rhythm == "信息层层推进"
    assert "内容探索" in result.segments[2].narration
    assert result.hook_alternatives[0] == "先抛核心问题"
