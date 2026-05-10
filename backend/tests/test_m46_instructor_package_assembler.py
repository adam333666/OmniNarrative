from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("DATABASE_URL", f"sqlite+pysqlite:///{Path('/tmp/multi_media_test.db')}")

from app.schemas.creation_request import CreationRequest
from app.schemas.narrative_package import ExpandedPackageScaffold, StructuredPackageScaffold
from app.schemas.profiles import AudienceProfile, StyleProfile
from app.schemas.trend_template import PlatformTrendTemplate
from app.services.package_assembler.service import PackageAssemblerService
from app.schemas.narrative_package import KeyShot, ScriptSegment
from app.services.structured_output_gateway.service import StructuredOutputGatewayService


class FakeInstructorClient:
    def create(self, **kwargs: object):
        response_model = kwargs.get("response_model")
        if response_model is ExpandedPackageScaffold:
            return ExpandedPackageScaffold.model_validate(
                {
                    "overview_expansion": {
                        "positioning_rationale": [
                            {
                                "title": "定位成立原因",
                                "detail": "主题同时具备高认知冲突和高讨论延展性。",
                                "purpose": "帮助策划确认题眼。",
                                "execution_hint": "先给问题，再给解释。",
                            }
                        ],
                        "audience_value_points": [
                            {
                                "title": "理解收益",
                                "detail": "让观众带走更清晰的判断框架。",
                                "purpose": "提升收藏和复述价值。",
                                "execution_hint": "每段保留一个可复述判断句。",
                            }
                        ],
                        "execution_priorities": [
                            {
                                "title": "优先级一",
                                "detail": "先把问题讲清楚，再追求表达风格。",
                            }
                        ],
                        "risk_controls": [
                            {
                                "title": "风险一",
                                "detail": "不要把封面和分发文案写成超长句。",
                            }
                        ],
                    },
                    "analysis_expansion": {
                        "audience_mindset_layers": [
                            {"title": "进入动机", "detail": "先被问题吸引，再决定是否继续听解释。"}
                        ],
                        "comprehension_barriers": [
                            {"title": "抽象门槛", "detail": "连续术语会导致观众掉线。"}
                        ],
                        "emotional_triggers": [
                            {"title": "认知冲突", "detail": "越反直觉，越容易引发停留。"}
                        ],
                        "trend_application_notes": [
                            {"title": "平台趋势落点", "detail": "完整解释链比纯结论更适合 B 站。"}
                        ],
                    },
                    "script_expansion": {
                        "expanded_segments": [
                            {
                                "segment_number": 1,
                                "narrative_function": "抓住注意力",
                                "expansion_goal": "把开头设问扩成更强的讨论起点。",
                                "transition_in": "直接用问题切进来。",
                                "transition_out": "把问题压到下一段解释上。",
                                "audience_psychology": "观众会先寻找一个明确判断。",
                                "detail_outline": ["先抛问题", "再给后果", "最后留判断"],
                                "delivery_notes": ["旁白不要先解释背景", "字幕突出判断句"],
                                "alt_narration_lines": ["先别急着回答，真正难的是后面那一步。"] ,
                                "visual_layers": ["问题字卡", "时间线关系图"],
                            }
                        ],
                        "expanded_key_shots": [
                            {
                                "shot_title": "钩子镜头",
                                "narrative_role": "开场抓人",
                                "composition_notes": "画面先给问题字幕，再补视觉信息。",
                                "motion_design": "快速推近后定住。",
                                "asset_layers": ["问题字卡", "主题关键词"],
                                "edit_variants": ["主版本完整保留", "切片版本只留结论句"],
                                "failure_fallback": "素材不够时保留问题字卡和字幕。",
                            }
                        ],
                        "title_strategy_notes": [
                            {"title": "标题策略", "detail": "主标题优先打问题，副标题补解释。"}
                        ],
                        "hook_strategy_notes": [
                            {"title": "开场策略", "detail": "3 秒内必须出现可复述的问题句。"}
                        ],
                        "retention_design_notes": [
                            {"title": "留存策略", "detail": "每段都要有小闭环。"}
                        ],
                    },
                    "multimodal_expansion": {
                        "scene_blueprints": [
                            {"title": "开场场景", "detail": "优先给冲突和异常感。"}
                        ],
                        "visual_motif_notes": [
                            {"title": "视觉母题", "detail": "重复使用时钟与回卷箭头。"}
                        ],
                        "audio_layering_notes": [
                            {"title": "音频层", "detail": "开场音乐不稳定，中段让位解释。"}
                        ],
                        "asset_pipeline_notes": [
                            {"title": "素材顺序", "detail": "先做信息卡，再做氛围镜头。"}
                        ],
                    },
                    "platform_expansion": {
                        "publishing_playbook": [
                            {"title": "首发玩法", "detail": "首发优先完整解释链。"}
                        ],
                        "comment_thread_playbook": [
                            {
                                "candidate_text": "你更接受哪一种解释？",
                                "usage_scenario": "置顶评论",
                                "design_reason": "先让观众站队。",
                            }
                        ],
                        "cover_iteration_notes": [
                            {"title": "封面控制", "detail": "封面只保留一个问题和一个结果词。"}
                        ],
                        "series_extension_angles": [
                            {
                                "candidate_text": "如果未来人已经来过，我们为什么没发现？",
                                "usage_scenario": "系列下一条",
                                "design_reason": "继续扩成观察型问题。",
                            }
                        ],
                        "release_rhythm_notes": [
                            {"title": "发布节奏", "detail": "首发后 24 小时内补问题回应。"}
                        ],
                    },
                    "machine_payload_expansion": {
                        "production_phases": [
                            {"title": "阶段一", "detail": "先锁问题句和 3 个核心判断。"}
                        ],
                        "shot_execution_notes": [
                            {
                                "shot_title": "钩子镜头",
                                "narrative_role": "开场抓人",
                                "composition_notes": "先问题，后细节。",
                                "motion_design": "快速推近。",
                                "asset_layers": ["问题字卡"],
                                "edit_variants": ["完整版本", "切片版本"],
                                "failure_fallback": "保留问题字幕。",
                            }
                        ],
                        "subtitle_strategy_notes": [
                            {"title": "字幕原则", "detail": "字幕只留判断句和转折句。"}
                        ],
                        "qa_checkpoints": [
                            {"title": "质检一", "detail": "前 3 秒必须讲明白问题。"}
                        ],
                        "fallback_actions": ["删修辞句，不删解释闭环。"],
                    },
                    "quality_control_notes": [
                        "不能破坏原有真值。",
                        "封面和分发文案必须可发布。",
                        "字幕、分镜、剪辑说明必须对齐。",
                    ],
                }
            )

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


class BrokenInstructorClient:
    def create(self, **_: object) -> StructuredPackageScaffold:
        raise RuntimeError("package assembly failed")


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


def test_package_assembler_prefers_instructor_scaffold() -> None:
    service = PackageAssemblerService(
        structured_output_gateway=StructuredOutputGatewayService(
            instructor_client_factory=FakeInstructorClient,
            provider_name="litellm",
            model_name="openai/gpt-4o-mini",
        )
    )

    result = service.build_result(
        generation_id="gen-m46",
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

    assert result.result_package.overview["design_summary"] == "先用问题吊起注意力，再用完整解释建立记忆点。"
    assert result.result_package.platform_layer["publishing_copy_suggestion"].startswith("如果你也想讲清时间旅行悖论")
    assert result.result_package.machine_payload_layer["thumbnail_prompt_block"] == "高对比封面，突出时间悖论冲突。"
    assert result.result_package.platform_layer["distribution_angles"][0] == "主版本强调认知冲突"
    assert result.result_package.platform_layer["cover_candidates"][0]["candidate_text"] == "时间旅行悖论到底卡在哪？"
    assert result.result_package.machine_payload_layer["storyboard_beats"][0] == "Beat 1: 设问"
    assert result.result_package.machine_payload_layer["storyboard_frames"][0]["beat_title"] == "设问起手"
    assert result.result_package.machine_payload_layer["storyboard_frames"][0]["linked_key_shot_title"] == "钩子镜头"
    assert result.result_package.machine_payload_layer["asset_preparation_notes"][0]["item_name"] == "问题字卡模板"
    assert result.result_package.machine_payload_layer["estimated_total_duration_seconds"] == 10
    assert result.analysis["key_design_decisions"][0] == "平台适配优先影响设问方式和解释链长度。"
    assert result.result_package.script_layer["segments"][0]["segment_title"] == "开头设问"
    assert result.result_package.overview["expanded_breakdown"]["positioning_rationale"][0]["title"] == "定位成立原因"
    assert result.analysis["expanded_analysis"]["audience_mindset_layers"][0]["title"] == "进入动机"
    assert result.result_package.script_layer["expanded_segments"][0]["narrative_function"] == "抓住注意力"
    assert result.result_package.platform_layer["expanded_distribution_playbook"]["publishing_playbook"][0]["title"] == "首发玩法"
    assert result.result_package.machine_payload_layer["expanded_execution_plan"]["production_phases"][0]["title"] == "阶段一"
    assert result.result_package.machine_payload_layer["quality_control_notes"][0] == "不能破坏原有真值。"
    assert result.analysis["runtime_diagnostics"]["package_assembly"]["source_type"] == "structured_output_gateway"


def test_package_assembler_falls_back_when_instructor_fails() -> None:
    service = PackageAssemblerService(
        structured_output_gateway=StructuredOutputGatewayService(
            instructor_client_factory=BrokenInstructorClient,
            provider_name="litellm",
            model_name="openai/gpt-4o-mini",
        )
    )

    result = service.build_result(
        generation_id="gen-m46-fallback",
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
        narrative_runtime={"source_type": "narrative_generator_fallback", "fallback_reason": "structured_output_unavailable_or_failed"},
    )

    assert result.result_package.overview["content_positioning"] == "science_popularization + bilibili 平台适配表达"
    assert result.result_package.multimodal_layer["scene_progression"][0] == "前 3 秒抛出核心问题"
    assert result.result_package.platform_layer["publish_timing_suggestions"][0] == "工作日晚间 19:00-22:00"
    assert result.result_package.machine_payload_layer["editing_checklist"][0] == "前 3 秒必须出现核心问题"
    assert result.result_package.machine_payload_layer["negative_constraints"] == ["铺垫过长", "只给结论不给推理"]
    assert result.result_package.platform_layer["distribution_angle_candidates"][0]["usage_scenario"] == "正式主视频分发"
    assert result.result_package.machine_payload_layer["voiceover_subtitle_alignment"][0]["linked_beat_number"] == 1
    assert result.result_package.machine_payload_layer["storyboard_frames"][0]["asset_requirement"] == "问题字卡模板 + 主题关键词动效"
    assert result.result_package.machine_payload_layer["storyboard_frames"][0]["linked_segment_number"] == 1
    assert result.result_package.machine_payload_layer["estimated_total_duration_seconds"] == 10
    assert result.analysis["key_design_decisions"][0] == "先保证结构完整与字段清晰，再逐步提高内容生成质量。"
    assert result.analysis["runtime_diagnostics"]["package_assembly"]["source_type"] == "package_assembler_fallback"


def test_package_assembler_fallback_tolerates_sparse_profiles_and_trends() -> None:
    service = PackageAssemblerService(
        structured_output_gateway=StructuredOutputGatewayService(
            instructor_client_factory=BrokenInstructorClient,
            provider_name="litellm",
            model_name="openai/gpt-4o-mini",
        )
    )

    sparse_audience = AudienceProfile(
        raw_text="18到28岁，喜欢科幻设定和逻辑推理的观众",
        age_group_guess="18-24",
        interest_tags=[],
        pain_points=[],
        content_preference=["开头要快"],
        emotion_preference=[],
    )
    sparse_trend = PlatformTrendTemplate(
        platform="bilibili",
        content_type="science_popularization",
        summary="近期 B 站更适合强设问开场和完整解释链。",
        hook_patterns=[],
        rhythm_patterns=[],
        title_cover_style=["设问式标题", "高信息密度封面"],
        audience_preference_summary="更偏好能快速进入问题、同时保留完整解释链的表达。",
        avoid_patterns=[],
        hot_topics_summary=["时间悖论", "世界观讨论"],
        source_type="manual_refresh_collected",
        updated_at="2026-03-27T00:00:00+00:00",
    )

    result = service.build_result(
        generation_id="gen-m46-sparse",
        request=build_request(),
        audience_profile=sparse_audience,
        style_profile=build_style(),
        trend_summary=sparse_trend,
        title="时间旅行悖论，为什么会让人越想越上头？",
        one_sentence_summary="一条兼顾理解与传播的结构化方案。",
        script_segments=build_segments(),
        key_shots=build_shots(),
        title_alternatives=["标题备选 A"],
        hook_alternatives=["钩子备选 A"],
        title_candidates=[],
        hook_candidates=[],
        narrative_runtime={"source_type": "narrative_generator_fallback", "fallback_reason": "structured_output_unavailable_or_failed"},
    )

    assert result.result_package.overview["target_audience_summary"] == "面向18-24人群，重点回应需要更快进入内容主题"
    assert result.result_package.platform_layer["audience_adaptation"] == "重点照顾内容探索与希望被带入但不被说教"
    assert result.result_package.platform_layer["hook_design_reason"] == "开头使用“先抛核心问题”以适应bilibili平台起手方式。"
    assert result.result_package.platform_layer["rhythm_structure_reason"] == "整体采用“信息层层推进”，避免铺垫过长。"
