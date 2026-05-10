from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("DATABASE_URL", f"sqlite+pysqlite:///{Path('/tmp/multi_media_test.db')}")

from app.schemas.creation_request import CreationRequest
from app.schemas.narrative_package import KeyShot, ScriptSegment, StructuredPackageScaffold
from app.schemas.profiles import AudienceProfile, StyleProfile
from app.schemas.trend_template import PlatformTrendTemplate, TrendSourceTraceItem
from app.services.export_payload.service import export_payload_service
from app.services.package_assembler.service import PackageAssemblerService
from app.services.structured_output_gateway.service import StructuredOutputGatewayService


class FakeInstructorClient:
    def create(self, **_: object) -> StructuredPackageScaffold:
        return StructuredPackageScaffold.model_validate(
            {
                "overview": {
                    "main_title": "时间旅行悖论，为什么会让人越想越上头？",
                    "one_sentence_summary": "一条兼顾理解与传播的结构化方案。",
                    "content_positioning": "science_popularization + bilibili 平台适配表达",
                    "target_platform": "bilibili",
                    "target_audience_summary": "面向18-24人群，重点回应复杂概念理解门槛高",
                    "style_summary": "suspense / 紧张好奇 / 强度 medium",
                    "design_summary": "先用问题吊起注意力，再用完整解释建立记忆点。",
                },
                "multimodal_layer": {
                    "characters": ["主讲述者", "世界观解释者"],
                    "scenes": ["设问开场", "世界观解释", "结尾反问"],
                    "visual_style": "高信息密度、强设问感的科幻讨论氛围",
                    "subtitle_style": "重点句放大，转折句单独停顿",
                    "audio_guides": ["开头压缩停顿", "中段加快解释", "结尾留一拍"],
                    "visual_keywords": ["时间旅行", "悖论", "逻辑推理"],
                    "rhythm_guidance": ["前段快速起势", "中段递进解释"],
                    "scene_progression": ["前 3 秒设问", "中段解释世界观", "结尾反问留白"],
                    "motion_cues": ["镜头快速推近", "解释段切信息卡", "结尾停留字幕"],
                    "asset_props": ["时间线图示", "设问字卡", "封面主文案"],
                    "visual_references": ["黑底高对比信息卡", "时间线关系示意图"],
                },
                "platform_layer": {
                    "platform_strategy": "近期 B 站更适合强设问开场和完整解释链。",
                    "trend_summary": {
                        "platform": "bilibili",
                        "content_type": "science_popularization",
                        "summary": "近期 B 站更适合强设问开场和完整解释链。",
                        "hook_patterns": ["先抛核心设问", "先给世界观矛盾"],
                        "rhythm_patterns": ["前段快速起势", "中段递进解释"],
                        "title_cover_style": ["设问式标题", "高信息密度封面"],
                        "audience_preference_summary": "更偏好能快速进入问题、同时保留完整解释链的表达。",
                        "avoid_patterns": ["铺垫过长", "只给结论不给推理"],
                        "hot_topics_summary": ["时间悖论", "世界观讨论"],
                        "source_type": "manual_refresh_collected",
                        "updated_at": "2026-03-27T00:00:00+00:00",
                    },
                    "audience_adaptation": "优先照顾脑洞设定兴趣和希望被带入但不被说教的情绪偏好。",
                    "hook_design_reason": "开头直接设问，贴合 B 站评论区补充推理的参与方式。",
                    "rhythm_structure_reason": "先快后稳，避免前半段铺垫过长。",
                    "title_cover_style": ["设问式标题", "高信息密度封面"],
                    "publishing_copy_suggestion": "如果你也想讲清时间旅行悖论，这个版本更适合 B 站。",
                    "avoid_patterns": ["铺垫过长", "只给结论不给推理"],
                    "cover_copy_alternatives": ["时间旅行悖论到底卡在哪？", "你以为懂了，其实还差关键一步"],
                    "comment_guidance": ["置顶评论补推理链", "结尾追问观众最认同的解释角度"],
                    "publish_timing_suggestions": ["工作日晚间 19:00-22:00", "周末下午 14:00-18:00"],
                    "distribution_angles": ["主版本强调认知冲突", "切片版本突出一句反常识结论"],
                    "thumbnail_copy_candidates": ["时间旅行悖论到底卡在哪？", "你以为懂了，其实还没"],
                    "cover_candidates": [
                        {
                            "candidate_text": "时间旅行悖论到底卡在哪？",
                            "usage_scenario": "封面首发",
                            "design_reason": "首发版本优先打认知冲突。",
                        }
                    ],
                    "distribution_angle_candidates": [
                        {
                            "candidate_text": "主版本强调认知冲突",
                            "usage_scenario": "主视频发布",
                            "design_reason": "更适合完整解释链。",
                        }
                    ],
                },
                "machine_payload_layer": {
                    "video_prompt_block": "围绕时间旅行悖论生成一条适配 bilibili 的视频叙事方案。",
                    "character_consistency_block": "保持讲述者理性、稳定且略带悬念感。",
                    "scene_description_block": "设问开场、解释推进、结尾留白的三段式科幻讨论场景。",
                    "style_constraints": ["suspense", "紧张好奇"],
                    "negative_constraints": ["铺垫过长", "只给结论不给推理"],
                    "key_shot_prompts": ["第一句问题", "关键解释镜头"],
                    "shot_duration_suggestions": [4, 6],
                    "thumbnail_prompt_block": "高对比封面，突出时间悖论冲突。",
                    "voiceover_prompt_block": "语气先快后稳，重点句停顿。",
                    "asset_checklist": ["封面主文案", "字幕关键词", "关系图"],
                    "editing_checklist": ["前 3 秒必须出现核心问题", "结尾保留评论引导字幕"],
                    "cta_variants": ["评论区告诉我你的答案", "想看下一版延展，先留下你的观点"],
                    "storyboard_beats": ["Beat 1: 设问", "Beat 2: 解释", "Beat 3: 留白"],
                    "storyboard_frames": [
                        {
                            "beat_number": 1,
                            "beat_title": "设问起手",
                            "linked_segment_number": 1,
                            "linked_key_shot_title": "钩子镜头",
                            "visual_focus": "高对比问题字幕",
                            "narration_focus": "先抛出反常识问题",
                            "estimated_duration_seconds": 3,
                            "asset_requirement": "问题字卡模板",
                            "editing_note": "开场硬切进入问题字幕",
                        }
                    ],
                    "asset_preparation_notes": [
                        {
                            "item_name": "问题字卡模板",
                            "linked_beat_number": 1,
                            "requirement_detail": "准备可替换主题词的高对比字卡",
                            "ready_stage": "生成前",
                        }
                    ],
                    "voiceover_subtitle_alignment": [
                        {
                            "linked_beat_number": 1,
                            "voiceover_line": "先抛出反常识问题",
                            "subtitle_line": "先抛出反常识问题",
                            "timing_note": "设问句整句同屏出现",
                        }
                    ],
                    "estimated_total_duration_seconds": 10,
                    "runtime_pacing_notes": ["前 3 秒完成设问起势"],
                },
                "key_design_decisions": [
                    "平台适配优先影响设问方式和解释链长度。",
                    "受众标签优先影响科幻信息密度与推理节奏。",
                    "机器层输出优先服务下游视频生成消费。",
                ],
            }
        )


def build_request() -> CreationRequest:
    return CreationRequest(
        theme_text="时间旅行悖论",
        content_type="science_popularization",
        target_platform="bilibili",
        target_audience_text="18到28岁，喜欢科幻设定和逻辑推理的观众",
        style_tone="suspense",
        custom_style_text="保持一点烧脑感",
    )


def build_audience() -> AudienceProfile:
    return AudienceProfile(
        raw_text="18到28岁，喜欢科幻设定和逻辑推理的观众",
        age_group_guess="18-24",
        interest_tags=["脑洞设定", "逻辑推理"],
        pain_points=["复杂概念理解门槛高"],
        content_preference=["开头要快"],
        emotion_preference=["希望被带入但不被说教"],
    )


def build_style() -> StyleProfile:
    return StyleProfile(
        style_label="suspense",
        emotion_label="紧张好奇",
        intensity_level="medium",
        custom_notes="保持一点烧脑感",
    )


def build_trend() -> PlatformTrendTemplate:
    return PlatformTrendTemplate(
        platform="bilibili",
        content_type="science_popularization",
        summary="近期 B 站更适合强设问开场和完整解释链。",
        hook_patterns=["先抛核心设问", "先给世界观矛盾"],
        rhythm_patterns=["前段快速起势", "中段递进解释"],
        title_cover_style=["设问式标题", "高信息密度封面"],
        audience_preference_summary="更偏好能快速进入问题、同时保留完整解释链的表达。",
        avoid_patterns=["铺垫过长", "只给结论不给推理"],
        hot_topics_summary=["时间悖论", "世界观讨论"],
        source_trace=[
            TrendSourceTraceItem(
                title="时间悖论又上热榜了",
                link="https://www.bilibili.com/video/BV1",
                excerpt="近期热门内容更强调强设问开场和完整解释链。",
                source_name="RSSHub / bilibili",
            )
        ],
        source_type="manual_refresh_collected",
        updated_at="2026-03-27T00:00:00+00:00",
    )


def build_segments() -> list[ScriptSegment]:
    return [
        ScriptSegment(
            segment_number=1,
            segment_title="开头设问",
            segment_goal="抓住注意力",
            narration="如果你回到过去改变一件小事，会不会把现在的你抹掉？",
            subtitle_text="改掉过去，今天的你还存在吗？",
            visual_description="设问字幕与时间隧道视觉交替出现。",
            emotion="紧张好奇",
            rhythm="前段快速起势",
        )
    ]


def build_shots() -> list[KeyShot]:
    return [
        KeyShot(
            shot_title="钩子镜头",
            shot_focus="第一句问题",
            shot_duration_seconds=4,
            transition_hint="直接切入",
        ),
        KeyShot(
            shot_title="解释镜头",
            shot_focus="关键解释镜头",
            shot_duration_seconds=6,
            transition_hint="从设问转入解释",
        ),
    ]


def build_result(api_key: str = "test-key"):
    service = PackageAssemblerService(
        structured_output_gateway=StructuredOutputGatewayService(
            instructor_client_factory=FakeInstructorClient,
            provider_name="litellm",
            model_name="openai/gpt-4o-mini",
            timeout_seconds=7.5,
        )
    )
    return service.build_result(
        generation_id="gen-m46-export",
        request=build_request(),
        audience_profile=build_audience(),
        style_profile=build_style(),
        trend_summary=build_trend(),
        title="时间旅行悖论，为什么会让人越想越上头？",
        one_sentence_summary="一条兼顾理解与传播的结构化方案。",
        script_segments=build_segments(),
        key_shots=build_shots(),
        title_alternatives=["标题备选 A"],
        hook_alternatives=["钩子备选 A"],
        title_candidates=[],
        hook_candidates=[],
        narrative_runtime={"source_type": "structured_output_gateway", "fallback_reason": None},
    )


def test_markdown_export_still_accepts_structured_package_output(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    result = build_result()

    markdown = export_payload_service.build_markdown(result)

    assert "多模态叙事结果包" in markdown
    assert "时间旅行悖论，为什么会让人越想越上头？" in markdown
    assert "平台适配层" in markdown
    assert "趋势依据与传播增强" in markdown
    assert "趋势来源轨迹" in markdown
    assert "制作执行蓝图" in markdown
    assert "关键镜头提示" in markdown
    assert "缩略图提示" in markdown
    assert "剪辑检查项" in markdown
    assert "标题结构化候选" in markdown
    assert "配音字幕对齐" in markdown
    assert "预计总时长" in markdown
    assert "结构化分镜帧" in markdown
    assert "对应关键镜头" in markdown
    assert "结构化素材准备项" in markdown
    assert "结构化配音字幕对齐" in markdown


def test_video_payload_export_still_accepts_structured_package_output(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    result = build_result()

    payload = export_payload_service.build_video_payload(result)

    assert payload.video_meta["title"] == "时间旅行悖论，为什么会让人越想越上头？"
    assert payload.video_meta["platform"] == "bilibili"
    assert payload.negative_constraints == ["铺垫过长", "只给结论不给推理"]
    assert payload.segments[0]["segment_title"] == "开头设问"
    assert payload.scene_progression == ["前 3 秒设问", "中段解释世界观", "结尾反问留白"]
    assert payload.thumbnail_copy_candidates[0] == "时间旅行悖论到底卡在哪？"
    assert payload.title_alternatives == ["标题备选 A"]
    assert payload.cta_variants[0] == "评论区告诉我你的答案"
    assert payload.cover_candidates[0]["candidate_text"] == "时间旅行悖论到底卡在哪？"
    assert payload.storyboard_beats[0] == "Beat 1: 设问"
    assert payload.storyboard_frames[0]["beat_title"] == "设问起手"
    assert payload.storyboard_frames[0]["linked_segment_number"] == 1
    assert payload.asset_preparation_notes[0]["item_name"] == "问题字卡模板"
    assert payload.voiceover_subtitle_alignment[0]["timing_note"] == "设问句整句同屏出现"
    assert payload.estimated_total_duration_seconds == 10
