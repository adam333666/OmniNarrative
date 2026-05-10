from __future__ import annotations

import logging
from datetime import UTC, datetime

from app.schemas.creation_request import CreationRequest
from app.schemas.narrative_package import (
    MachinePayloadLayer,
    MultimodalLayer,
    NarrativePackage,
    OverviewLayer,
    PlatformLayer,
    ResultEnvelope,
    ScriptLayer,
    AssetPreparationItem,
    StoryboardFrame,
    StructuredTextCandidate,
    StructuredPackageScaffold,
    VoiceoverSubtitleAlignmentItem,
)
from app.schemas.profiles import AudienceProfile, StyleProfile
from app.schemas.trend_template import PlatformTrendTemplate
from app.services.package_expander.service import PackageExpanderService
from app.services.structured_output_gateway.service import (
    StructuredOutputGatewayService,
    structured_output_gateway_service,
)

logger = logging.getLogger(__name__)


class PackageAssemblerService:
    def __init__(
        self,
        structured_output_gateway: StructuredOutputGatewayService | None = None,
        package_expander: PackageExpanderService | None = None,
    ) -> None:
        self.structured_output_gateway = structured_output_gateway or structured_output_gateway_service
        self.package_expander = package_expander or PackageExpanderService(
            structured_output_gateway=self.structured_output_gateway
        )

    def build_result(
        self,
        generation_id: str,
        request: CreationRequest,
        audience_profile: AudienceProfile,
        style_profile: StyleProfile,
        trend_summary: PlatformTrendTemplate,
        title: str,
        one_sentence_summary: str,
        script_segments,
        key_shots,
        title_alternatives,
        hook_alternatives,
        title_candidates,
        hook_candidates,
        narrative_runtime: dict[str, str | None] | None = None,
    ) -> ResultEnvelope:
        generated_at = datetime.now(UTC)
        script_layer = self._build_script_layer(
            script_segments=script_segments,
            key_shots=key_shots,
            title_alternatives=title_alternatives,
            hook_alternatives=hook_alternatives,
            title_candidates=title_candidates,
            hook_candidates=hook_candidates,
        )

        structured_scaffold = self._build_structured_scaffold(
            request=request,
            audience_profile=audience_profile,
            style_profile=style_profile,
            trend_summary=trend_summary,
            title=title,
            one_sentence_summary=one_sentence_summary,
            script_layer=script_layer,
        )
        scaffold = structured_scaffold or self._build_fallback_scaffold(
            request=request,
            audience_profile=audience_profile,
            style_profile=style_profile,
            trend_summary=trend_summary,
            title=title,
            one_sentence_summary=one_sentence_summary,
            key_shots=key_shots,
        )
        package_runtime = {
            "source_type": "structured_output_gateway" if structured_scaffold is not None else "package_assembler_fallback",
            "fallback_reason": None if structured_scaffold is not None else "structured_output_unavailable_or_failed",
        }

        result_package = NarrativePackage(
            overview=scaffold.overview.model_dump(),
            script_layer=script_layer.model_dump(),
            multimodal_layer=scaffold.multimodal_layer.model_dump(),
            platform_layer=scaffold.platform_layer.model_dump(),
            machine_payload_layer=scaffold.machine_payload_layer.model_dump(),
        )
        expansion_scaffold, expansion_runtime = self.package_expander.build_expansion(
            request=request,
            audience_profile=audience_profile,
            style_profile=style_profile,
            trend_summary=trend_summary,
            overview=result_package.overview,
            script_layer=result_package.script_layer,
            multimodal_layer=result_package.multimodal_layer,
            platform_layer=result_package.platform_layer,
            machine_payload_layer=result_package.machine_payload_layer,
        )
        self._merge_expansion_into_result(
            result_package=result_package,
            expansion_scaffold=expansion_scaffold,
        )

        return ResultEnvelope(
            request_summary=request.model_dump(),
            analysis={
                "audience_profile": audience_profile.model_dump(),
                "style_profile": style_profile.model_dump(),
                "trend_summary": trend_summary.model_dump(),
                "key_design_decisions": scaffold.key_design_decisions,
                "expanded_analysis": expansion_scaffold.analysis_expansion.model_dump(),
                "runtime_diagnostics": {
                    "narrative_generation": narrative_runtime
                    or {
                        "source_type": "unknown",
                        "fallback_reason": None,
                    },
                    "package_assembly": package_runtime,
                    "package_expansion": expansion_runtime,
                },
            },
            result_package=result_package,
            export_meta={
                "schema_version": "0.1.0",
                "generation_id": generation_id,
                "generated_at": generated_at.isoformat(),
            },
        )

    def _merge_expansion_into_result(
        self,
        *,
        result_package: NarrativePackage,
        expansion_scaffold,
    ) -> None:
        result_package.overview["expanded_breakdown"] = expansion_scaffold.overview_expansion.model_dump()
        result_package.script_layer["expanded_segments"] = [
            item.model_dump() for item in expansion_scaffold.script_expansion.expanded_segments
        ]
        result_package.script_layer["expanded_key_shots"] = [
            item.model_dump() for item in expansion_scaffold.script_expansion.expanded_key_shots
        ]
        result_package.script_layer["title_strategy_notes"] = [
            item.model_dump() for item in expansion_scaffold.script_expansion.title_strategy_notes
        ]
        result_package.script_layer["hook_strategy_notes"] = [
            item.model_dump() for item in expansion_scaffold.script_expansion.hook_strategy_notes
        ]
        result_package.script_layer["retention_design_notes"] = [
            item.model_dump() for item in expansion_scaffold.script_expansion.retention_design_notes
        ]
        result_package.multimodal_layer["expanded_visual_plan"] = expansion_scaffold.multimodal_expansion.model_dump()
        result_package.platform_layer["expanded_distribution_playbook"] = expansion_scaffold.platform_expansion.model_dump()
        result_package.machine_payload_layer["expanded_execution_plan"] = expansion_scaffold.machine_payload_expansion.model_dump()
        result_package.machine_payload_layer["quality_control_notes"] = list(expansion_scaffold.quality_control_notes)

    def _build_script_layer(
        self,
        *,
        script_segments,
        key_shots,
        title_alternatives,
        hook_alternatives,
        title_candidates,
        hook_candidates,
    ) -> ScriptLayer:
        derived_title_candidates = list(title_candidates) or [
            self._build_candidate(
                candidate_text=item,
                usage_scenario=scenario,
                design_reason=reason,
            )
            for item, scenario, reason in zip(
                list(title_alternatives)[:3],
                ["主发布标题", "封面联动标题", "二次分发标题"],
                ["直接承接主发布标题版本。", "适合和封面文案联动测试。", "适合做二次分发与合集页复用。"],
                strict=False,
            )
        ]
        derived_hook_candidates = list(hook_candidates) or [
            self._build_candidate(
                candidate_text=item,
                usage_scenario=scenario,
                design_reason=reason,
            )
            for item, scenario, reason in zip(
                list(hook_alternatives)[:3],
                ["正片开场", "口播起手", "切片复用"],
                ["优先服务正片前 3 秒抓人。", "更适合讲述者直接起手口播。", "适合后续短切片复用。"],
                strict=False,
            )
        ]
        return ScriptLayer(
            segments=list(script_segments),
            key_shots=list(key_shots),
            script_note="当前脚本层以 narrative_generator 产物为真值，package_assembler 仅做结构化承接。",
            title_alternatives=list(title_alternatives),
            hook_alternatives=list(hook_alternatives),
            title_candidates=derived_title_candidates,
            hook_candidates=derived_hook_candidates,
        )

    def _build_structured_scaffold(
        self,
        *,
        request: CreationRequest,
        audience_profile: AudienceProfile,
        style_profile: StyleProfile,
        trend_summary: PlatformTrendTemplate,
        title: str,
        one_sentence_summary: str,
        script_layer: ScriptLayer,
    ) -> StructuredPackageScaffold | None:
        return self.structured_output_gateway.generate(
            caller_name="package_assembler",
            response_model=StructuredPackageScaffold,
            messages=self._build_structured_messages(
                request=request,
                audience_profile=audience_profile,
                style_profile=style_profile,
                trend_summary=trend_summary,
                title=title,
                one_sentence_summary=one_sentence_summary,
                script_layer=script_layer,
            ),
        )

    def _build_structured_messages(
        self,
        *,
        request: CreationRequest,
        audience_profile: AudienceProfile,
        style_profile: StyleProfile,
        trend_summary: PlatformTrendTemplate,
        title: str,
        one_sentence_summary: str,
        script_layer: ScriptLayer,
    ) -> list[dict[str, str]]:
        return [
            {
                "role": "system",
                "content": (
                    "你是多模态结果包组装器。"
                    "请严格输出可被 Pydantic StructuredPackageScaffold 校验通过的结构化结果。"
                    "script_layer 已经由上游生成，本次只负责 overview、multimodal_layer、platform_layer、machine_payload_layer 和 key_design_decisions。"
                    "所有文案使用简洁、可执行的中文。"
                    "结果包必须足够重，能直接用于演示、评审和下游制作交接。"
                    "请尽量把多模态执行提示、发布动作建议、素材道具清单、封面候选、分发角度、剪辑检查项、storyboard_beats、asset_preparation_notes、voiceover_subtitle_alignment 和评论区互动引导补完整。"
                    "cover_candidates 与 distribution_angle_candidates 需要输出结构化候选，不要只返回字符串数组。"
                    "不要解释，不要输出 schema 之外的字段。"
                ),
            },
            {
                "role": "user",
                "content": (
                    f"主题: {request.theme_text}\n"
                    f"内容类型: {request.content_type}\n"
                    f"目标平台: {request.target_platform}\n"
                    f"主标题: {title}\n"
                    f"一句话摘要: {one_sentence_summary}\n"
                    f"受众画像: {audience_profile.model_dump_json()}\n"
                    f"风格画像: {style_profile.model_dump_json()}\n"
                    f"趋势模板: {trend_summary.model_dump_json()} \n"
                    f"脚本层真值: {script_layer.model_dump_json()}\n"
                    "请基于这些真值组装结果包其他层，并让设计决策解释清楚平台适配、受众适配和多模态下游可执行性。"
                ),
            },
        ]

    def _build_fallback_scaffold(
        self,
        *,
        request: CreationRequest,
        audience_profile: AudienceProfile,
        style_profile: StyleProfile,
        trend_summary: PlatformTrendTemplate,
        title: str,
        one_sentence_summary: str,
        key_shots,
    ) -> StructuredPackageScaffold:
        audience_profile = self._normalize_audience_profile(audience_profile)
        trend_summary = self._normalize_trend_summary(trend_summary)
        return StructuredPackageScaffold(
            overview=OverviewLayer(
                main_title=title,
                one_sentence_summary=one_sentence_summary,
                content_positioning=f"{request.content_type} + {trend_summary.platform} 平台适配表达",
                target_platform=request.target_platform,
                target_audience_summary=f"面向{audience_profile.age_group_guess}人群，重点回应{audience_profile.pain_points[0]}",
                style_summary=f"{style_profile.style_label} / {style_profile.emotion_label} / 强度 {style_profile.intensity_level}",
                design_summary="先抓住注意力，再完成解释，最后留下可转发的余味。",
            ),
            multimodal_layer=MultimodalLayer(
                characters=["主讲述者", "观众代入视角角色"],
                scenes=["开头钩子场景", "解释场景", "收束场景"],
                visual_style=f"围绕{style_profile.emotion_label}构建统一视觉氛围",
                subtitle_style="高对比、大字号、重点句保留停顿感",
                audio_guides=["开头快速进入", "解释段保持节奏层次", "结尾减速留白"],
                visual_keywords=audience_profile.interest_tags,
                rhythm_guidance=trend_summary.rhythm_patterns,
                scene_progression=["前 3 秒抛出核心问题", "中段拆解关键冲突", "结尾留下可讨论的开放问题"],
                motion_cues=["开场快速推近", "解释段配合信息卡分层出现", "结尾轻微减速并停留字幕"],
                asset_props=["平台关键词字幕卡", "高对比封面字卡", "核心概念关系箭头图"],
                visual_references=["黑底高对比信息卡", "时间线关系示意图", "评论区观点摘录叠层"],
            ),
            platform_layer=PlatformLayer(
                platform_strategy=trend_summary.summary,
                trend_summary=trend_summary,
                audience_adaptation=f"重点照顾{audience_profile.interest_tags[0]}与{audience_profile.emotion_preference[0]}",
                hook_design_reason=f"开头使用“{trend_summary.hook_patterns[0]}”以适应{trend_summary.platform}平台起手方式。",
                rhythm_structure_reason=f"整体采用“{trend_summary.rhythm_patterns[0]}”，避免{trend_summary.avoid_patterns[0]}。",
                title_cover_style=trend_summary.title_cover_style,
                publishing_copy_suggestion=f"如果你也在想{request.theme_text}，这条内容会帮你更快抓住真正的问题。",
                avoid_patterns=trend_summary.avoid_patterns,
                cover_copy_alternatives=[
                    f"你真的理解{request.theme_text}了吗？",
                    f"{request.theme_text}最容易被忽略的那一层",
                ],
                comment_guidance=[
                    f"结尾主动追问观众最认同的{request.theme_text}解释角度。",
                    "在置顶评论补充一条最容易被忽略的推理链。",
                ],
                publish_timing_suggestions=["工作日晚间 19:00-22:00", "周末下午 14:00-18:00"],
                distribution_angles=[
                    f"主版本强调{request.theme_text}的认知冲突",
                    "切片版本突出最反常识的一句结论",
                    "评论区延展版本主打补充反例与世界观",
                ],
                thumbnail_copy_candidates=[
                    f"{request.theme_text}到底卡在哪？",
                    f"你以为懂了{request.theme_text}，其实还没",
                ],
                cover_candidates=[
                    self._build_candidate(
                        candidate_text=f"你真的理解{request.theme_text}了吗？",
                        usage_scenario="封面主文案首发版本",
                        design_reason="优先用设问方式承接平台封面风格，适合首页首发。",
                    ),
                    self._build_candidate(
                        candidate_text=f"{request.theme_text}最容易被忽略的那一层",
                        usage_scenario="封面二测版本",
                        design_reason="强调认知落差，适合二次测试点击率。",
                    ),
                ],
                distribution_angle_candidates=[
                    self._build_candidate(
                        candidate_text=f"主版本强调{request.theme_text}的认知冲突",
                        usage_scenario="正式主视频分发",
                        design_reason="优先打认知冲突，适合长视频主发布。",
                    ),
                    self._build_candidate(
                        candidate_text="切片版本突出最反常识的一句结论",
                        usage_scenario="短切片二次分发",
                        design_reason="保留最强结论句，方便在短切片里单独成立。",
                    ),
                    self._build_candidate(
                        candidate_text="评论区延展版本主打补充反例与世界观",
                        usage_scenario="评论区与合集页延展",
                        design_reason="把世界观讨论往评论区引，增强互动深度。",
                    ),
                ],
            ),
            machine_payload_layer=MachinePayloadLayer(
                video_prompt_block=f"围绕{request.theme_text}生成一条适配{request.target_platform}的视频叙事方案。",
                character_consistency_block="保持叙述者形象统一，语气稳定。",
                scene_description_block="开头冲击、中段解释、结尾留白三段式场景推进。",
                style_constraints=[style_profile.style_label, style_profile.emotion_label],
                negative_constraints=trend_summary.avoid_patterns,
                key_shot_prompts=[shot.shot_focus for shot in key_shots],
                shot_duration_suggestions=[shot.shot_duration_seconds for shot in key_shots],
                thumbnail_prompt_block=f"为{request.target_platform}生成高对比、强设问式封面，突出{request.theme_text}的矛盾感。",
                voiceover_prompt_block=f"旁白语气保持{style_profile.emotion_label}，先快后稳，重点句做短暂停顿。",
                asset_checklist=["封面主文案 1 条", "字幕关键词 3 组", "关系图/示意图 2 张", "结尾评论引导字幕 1 条"],
                editing_checklist=["前 3 秒必须出现核心问题", "中段至少一次切换信息卡", "结尾保留评论引导字幕"],
                cta_variants=["评论区告诉我你的答案", "如果你也卡在这里，继续往下聊", "想看下一版延展，先留下你的观点"],
                storyboard_beats=[
                    "Beat 1: 0-3 秒只保留核心设问和冲突字幕。",
                    "Beat 2: 4-10 秒切入解释框架与关系图。",
                    "Beat 3: 11 秒后收束为评论区可延展的问题。",
                ],
                storyboard_frames=[
                    StoryboardFrame(
                        beat_number=1,
                        beat_title="设问起手",
                        linked_segment_number=1,
                        linked_key_shot_title="钩子镜头",
                        visual_focus="高对比问题字幕 + 主题关键词冲击入场",
                        narration_focus="先把反常识问题完整抛出，不做背景铺垫",
                        estimated_duration_seconds=3,
                        asset_requirement="问题字卡模板 + 主题关键词动效",
                        editing_note="开场必须硬切进问题字幕，避免淡入拖节奏",
                    ),
                    StoryboardFrame(
                        beat_number=2,
                        beat_title="解释展开",
                        linked_segment_number=2,
                        linked_key_shot_title="解释镜头",
                        visual_focus="关系图示卡 + 受众场景补充画面",
                        narration_focus="把核心矛盾拆成两层解释，并给出受众可理解的桥接句",
                        estimated_duration_seconds=6,
                        asset_requirement="关系图素材 + 受众代入场景镜头",
                        editing_note="解释段至少切一次信息卡，保证节奏层次",
                    ),
                    StoryboardFrame(
                        beat_number=3,
                        beat_title="结尾收束",
                        linked_segment_number=4,
                        linked_key_shot_title="结尾镜头",
                        visual_focus="结尾判断字幕 + 评论引导卡停留",
                        narration_focus="用一句可讨论的判断收束，并把讨论引向评论区",
                        estimated_duration_seconds=6,
                        asset_requirement="结尾评论引导卡 + 留白字幕版",
                        editing_note="结尾字幕要单独停留一拍，给评论引导留空间",
                    ),
                ],
                asset_preparation_notes=[
                    AssetPreparationItem(
                        item_name="问题字卡模板",
                        linked_beat_number=1,
                        requirement_detail="准备可直接替换主题词的高对比问题字卡模板。",
                        ready_stage="生成前",
                    ),
                    AssetPreparationItem(
                        item_name="关系图透明底素材",
                        linked_beat_number=2,
                        requirement_detail="关系图素材需保留透明底版本，方便后续动画叠加。",
                        ready_stage="剪辑前",
                    ),
                    AssetPreparationItem(
                        item_name="评论引导字幕版",
                        linked_beat_number=3,
                        requirement_detail="评论引导字幕建议单独导出一版，便于结尾快速替换。",
                        ready_stage="导出前",
                    ),
                ],
                voiceover_subtitle_alignment=[
                    VoiceoverSubtitleAlignmentItem(
                        linked_beat_number=1,
                        voiceover_line="如果结果会先于原因出现，你还敢相信时间吗？",
                        subtitle_line="如果结果会先于原因出现，你还敢相信时间吗？",
                        timing_note="设问句整句同屏，不拆分字幕。",
                    ),
                    VoiceoverSubtitleAlignmentItem(
                        linked_beat_number=2,
                        voiceover_line="真正卡住你的，不是答案，是那一步推理转弯。",
                        subtitle_line="真正卡住你的，是那一步推理转弯。",
                        timing_note="转折句单独成条，并与信息卡同步切换。",
                    ),
                    VoiceoverSubtitleAlignmentItem(
                        linked_beat_number=3,
                        voiceover_line="如果你是片中的主角，你会怎么选？",
                        subtitle_line="你会怎么选？",
                        timing_note="结尾判断和评论引导错一拍出现，保留余味停顿。",
                    ),
                ],
                estimated_total_duration_seconds=sum(shot.shot_duration_seconds for shot in key_shots),
                runtime_pacing_notes=[
                    "前 3 秒必须完成设问起势，不能先铺背景。",
                    "中段解释控制在主体时长的 50% 左右，避免信息过载。",
                    "结尾至少留出 1 个停顿节拍给评论引导字幕。",
                ],
            ),
            key_design_decisions=[
                "先保证结构完整与字段清晰，再逐步提高内容生成质量。",
                "平台适配优先影响开头钩子、节奏结构与标题封面风格。",
                "受众标签优先影响解释方式与结尾收束语气。",
            ],
        )

    def _normalize_audience_profile(self, audience_profile: AudienceProfile) -> AudienceProfile:
        return audience_profile.model_copy(
            update={
                "pain_points": self._coalesce_string_list(audience_profile.pain_points, ["需要更快进入内容主题"]),
                "interest_tags": self._coalesce_string_list(audience_profile.interest_tags, ["内容探索"]),
                "emotion_preference": self._coalesce_string_list(
                    audience_profile.emotion_preference,
                    ["希望被带入但不被说教"],
                ),
            }
        )

    def _normalize_trend_summary(self, trend_summary: PlatformTrendTemplate) -> PlatformTrendTemplate:
        return trend_summary.model_copy(
            update={
                "hook_patterns": self._coalesce_string_list(trend_summary.hook_patterns, ["先抛核心问题"]),
                "rhythm_patterns": self._coalesce_string_list(trend_summary.rhythm_patterns, ["信息层层推进"]),
                "avoid_patterns": self._coalesce_string_list(trend_summary.avoid_patterns, ["铺垫过长"]),
            }
        )

    def _coalesce_string_list(self, values: list[str], fallback: list[str]) -> list[str]:
        cleaned = [item.strip() for item in values if item.strip()]
        return cleaned or list(fallback)

    def _build_candidate(
        self,
        *,
        candidate_text: str,
        usage_scenario: str,
        design_reason: str,
    ) -> StructuredTextCandidate:
        return StructuredTextCandidate(
            candidate_text=candidate_text,
            usage_scenario=usage_scenario,
            design_reason=design_reason,
        )


package_assembler_service = PackageAssemblerService()
