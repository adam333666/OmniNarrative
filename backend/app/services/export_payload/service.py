from app.schemas.narrative_package import ResultEnvelope
from app.schemas.video_payload import VideoGenerationPayload


class ExportPayloadService:
    def _append_candidate_lines(self, lines: list[str], heading: str, candidates: list[dict]) -> None:
        if not candidates:
            return

        lines.append(heading)
        for candidate in candidates:
            lines.extend(
                [
                    f"- 文案：{candidate.get('candidate_text', '')}",
                    f"  - 使用场景：{candidate.get('usage_scenario', '')}",
                    f"  - 设计原因：{candidate.get('design_reason', '')}",
                ]
            )
        lines.append("")

    def _append_detail_items(self, lines: list[str], heading: str, items: list[dict]) -> None:
        if not items:
            return

        lines.append(heading)
        for item in items:
            lines.append(f"- {item.get('title', '')}：{item.get('detail', '')}")
            if item.get("purpose"):
                lines.append(f"  - 作用：{item.get('purpose', '')}")
            if item.get("execution_hint"):
                lines.append(f"  - 执行提示：{item.get('execution_hint', '')}")
        lines.append("")

    def build_markdown(self, result: ResultEnvelope) -> str:
        overview = result.result_package.overview
        script_layer = result.result_package.script_layer
        platform_layer = result.result_package.platform_layer
        multimodal_layer = result.result_package.multimodal_layer
        machine_payload_layer = result.result_package.machine_payload_layer
        analysis = result.analysis
        overview_expansion = overview.get("expanded_breakdown", {})
        analysis_expansion = analysis.get("expanded_analysis", {})
        script_expanded_segments = script_layer.get("expanded_segments", [])
        script_expanded_key_shots = script_layer.get("expanded_key_shots", [])
        multimodal_expansion = multimodal_layer.get("expanded_visual_plan", {})
        platform_expansion = platform_layer.get("expanded_distribution_playbook", {})
        machine_payload_expansion = machine_payload_layer.get("expanded_execution_plan", {})

        lines = [
            "# 多模态叙事结果包",
            "",
            "## 项目总览层",
            f"- 主标题：{overview['main_title']}",
            f"- 一句话梗概：{overview['one_sentence_summary']}",
            f"- 内容定位：{overview['content_positioning']}",
            f"- 目标平台：{overview['target_platform']}",
            f"- 风格摘要：{overview['style_summary']}",
            "",
            "## 中间分析摘要",
            f"- 受众原文：{analysis['audience_profile']['raw_text']}",
            f"- 年龄猜测：{analysis['audience_profile']['age_group_guess']}",
            f"- 兴趣标签：{' / '.join(analysis['audience_profile']['interest_tags'])}",
            f"- 趋势摘要：{analysis['trend_summary']['summary']}",
            "",
            "## 趋势依据与传播增强",
            f"- 趋势钩子：{' / '.join(analysis['trend_summary']['hook_patterns'])}",
            f"- 趋势节奏：{' / '.join(analysis['trend_summary']['rhythm_patterns'])}",
            f"- 标题/封面风格：{' / '.join(analysis['trend_summary']['title_cover_style'])}",
            f"- 受众偏好摘要：{analysis['trend_summary']['audience_preference_summary']}",
            f"- 规避方向：{' / '.join(analysis['trend_summary']['avoid_patterns'])}",
            f"- 热点线索：{' / '.join(analysis['trend_summary']['hot_topics_summary'])}",
            f"- 互动模式：{' / '.join(analysis['trend_summary'].get('interaction_patterns', []))}",
            f"- 情绪切口：{' / '.join(analysis['trend_summary'].get('emotional_entry_points', []))}",
            f"- 创作者角度：{analysis['trend_summary'].get('creator_angle_summary', '')}",
            "",
        ]

        self._append_detail_items(lines, "### 总览扩写：定位依据", overview_expansion.get("positioning_rationale", []))
        self._append_detail_items(lines, "### 总览扩写：用户价值", overview_expansion.get("audience_value_points", []))
        self._append_detail_items(lines, "### 总览扩写：执行优先级", overview_expansion.get("execution_priorities", []))
        self._append_detail_items(lines, "### 总览扩写：风险控制", overview_expansion.get("risk_controls", []))
        self._append_detail_items(lines, "### 分析扩写：受众心理层", analysis_expansion.get("audience_mindset_layers", []))
        self._append_detail_items(lines, "### 分析扩写：理解障碍", analysis_expansion.get("comprehension_barriers", []))
        self._append_detail_items(lines, "### 分析扩写：情绪触发器", analysis_expansion.get("emotional_triggers", []))
        self._append_detail_items(lines, "### 分析扩写：趋势应用说明", analysis_expansion.get("trend_application_notes", []))

        lines.extend(
            [
            "## 叙事脚本层",
            ]
        )

        source_trace = analysis["trend_summary"].get("source_trace", [])
        if source_trace:
            lines.extend(["### 趋势来源轨迹"])
            for item in source_trace:
                lines.extend(
                    [
                        f"- 来源：{item.get('source_name', 'unknown')}",
                        f"  - 标题：{item.get('title', '')}",
                        f"  - 摘录：{item.get('excerpt', '')}",
                        f"  - 链接：{item.get('link', '') or '无'}",
                    ]
                )
            lines.append("")

        for segment in script_layer['segments']:
            lines.extend(
                [
                    f"### 段落 {segment['segment_number']}：{segment['segment_title']}",
                    f"- 段落目标：{segment['segment_goal']}",
                    f"- 旁白：{segment['narration']}",
                    f"- 字幕：{segment['subtitle_text']}",
                    f"- 画面：{segment['visual_description']}",
                    f"- 情绪 / 节奏：{segment['emotion']} / {segment['rhythm']}",
                    "",
                ]
            )

        if script_expanded_segments:
            lines.append("### 段落扩写说明")
            for segment in script_expanded_segments:
                lines.extend(
                    [
                        f"- 段落 {segment.get('segment_number', '')}",
                        f"  - 叙事功能：{segment.get('narrative_function', '')}",
                        f"  - 扩写目标：{segment.get('expansion_goal', '')}",
                        f"  - 前接：{segment.get('transition_in', '')}",
                        f"  - 后接：{segment.get('transition_out', '')}",
                        f"  - 观众心理：{segment.get('audience_psychology', '')}",
                        f"  - 细纲：{' / '.join(segment.get('detail_outline', []))}",
                        f"  - 讲述提示：{' / '.join(segment.get('delivery_notes', []))}",
                        f"  - 替代旁白：{' / '.join(segment.get('alt_narration_lines', []))}",
                        f"  - 视觉层次：{' / '.join(segment.get('visual_layers', []))}",
                    ]
                )
            lines.append("")

        if script_expanded_key_shots:
            lines.append("### 关键镜头扩写说明")
            for shot in script_expanded_key_shots:
                lines.extend(
                    [
                        f"- 镜头：{shot.get('shot_title', '')}",
                        f"  - 叙事角色：{shot.get('narrative_role', '')}",
                        f"  - 构图说明：{shot.get('composition_notes', '')}",
                        f"  - 运动设计：{shot.get('motion_design', '')}",
                        f"  - 资产层：{' / '.join(shot.get('asset_layers', []))}",
                        f"  - 剪辑变体：{' / '.join(shot.get('edit_variants', []))}",
                        f"  - 失败回退：{shot.get('failure_fallback', '')}",
                    ]
                )
            lines.append("")

        self._append_candidate_lines(lines, "### 标题结构化候选", script_layer.get("title_candidates", []))
        self._append_candidate_lines(lines, "### 开场钩子结构化候选", script_layer.get("hook_candidates", []))
        self._append_detail_items(lines, "### 标题策略扩写", script_layer.get("title_strategy_notes", []))
        self._append_detail_items(lines, "### 钩子策略扩写", script_layer.get("hook_strategy_notes", []))
        self._append_detail_items(lines, "### 留存设计扩写", script_layer.get("retention_design_notes", []))

        lines.extend(
            [
                "## 平台适配层",
                f"- 平台策略：{platform_layer['platform_strategy']}",
                f"- 受众适配：{platform_layer['audience_adaptation']}",
                f"- 钩子设计原因：{platform_layer['hook_design_reason']}",
                f"- 节奏结构原因：{platform_layer['rhythm_structure_reason']}",
                f"- 发布文案建议：{platform_layer['publishing_copy_suggestion']}",
                f"- 不建议表达：{' / '.join(platform_layer['avoid_patterns'])}",
                f"- 发布时间建议：{' / '.join(platform_layer.get('publish_timing_suggestions', []))}",
                f"- 分发角度：{' / '.join(platform_layer.get('distribution_angles', []))}",
                f"- 封面文案候选：{' / '.join(platform_layer.get('thumbnail_copy_candidates', []))}",
                f"- 标题备选：{' / '.join(script_layer.get('title_alternatives', []))}",
                f"- 开场钩子备选：{' / '.join(script_layer.get('hook_alternatives', []))}",
                f"- 封面文案备选：{' / '.join(platform_layer.get('cover_copy_alternatives', []))}",
                f"- 评论区引导：{' / '.join(platform_layer.get('comment_guidance', []))}",
                "",
                "## 制作执行蓝图",
                f"- 场景推进：{' / '.join(multimodal_layer.get('scene_progression', []))}",
                f"- 运动提示：{' / '.join(multimodal_layer.get('motion_cues', []))}",
                f"- 素材道具：{' / '.join(multimodal_layer.get('asset_props', []))}",
                f"- 视觉参考：{' / '.join(multimodal_layer.get('visual_references', []))}",
                f"- 角色一致性：{machine_payload_layer.get('character_consistency_block', '')}",
                f"- 场景描述提示：{machine_payload_layer.get('scene_description_block', '')}",
                f"- 关键镜头提示：{' / '.join(machine_payload_layer.get('key_shot_prompts', []))}",
                f"- 镜头时长建议：{' / '.join([str(item) for item in machine_payload_layer.get('shot_duration_suggestions', [])])}",
                f"- 缩略图提示：{machine_payload_layer.get('thumbnail_prompt_block', '')}",
                f"- 配音提示：{machine_payload_layer.get('voiceover_prompt_block', '')}",
                f"- 素材清单：{' / '.join(machine_payload_layer.get('asset_checklist', []))}",
                f"- 剪辑检查项：{' / '.join(machine_payload_layer.get('editing_checklist', []))}",
                f"- CTA 变体：{' / '.join(machine_payload_layer.get('cta_variants', []))}",
                f"- 分镜节拍：{' / '.join(machine_payload_layer.get('storyboard_beats', []))}",
                f"- 预计总时长：{machine_payload_layer.get('estimated_total_duration_seconds', 0)} 秒",
                f"- 节奏说明：{' / '.join(machine_payload_layer.get('runtime_pacing_notes', []))}",
            ]
        )

        storyboard_frames = machine_payload_layer.get("storyboard_frames", [])
        if storyboard_frames:
            lines.append("### 结构化分镜帧")
            for frame in storyboard_frames:
                lines.extend(
                    [
                        f"- 分镜 {frame.get('beat_number', '')}：{frame.get('beat_title', '')}",
                        f"  - 对应段落：{frame.get('linked_segment_number', '')}",
                        f"  - 对应关键镜头：{frame.get('linked_key_shot_title', '') or '无'}",
                        f"  - 画面焦点：{frame.get('visual_focus', '')}",
                        f"  - 旁白焦点：{frame.get('narration_focus', '')}",
                        f"  - 预计时长：{frame.get('estimated_duration_seconds', 0)} 秒",
                        f"  - 素材要求：{frame.get('asset_requirement', '')}",
                        f"  - 剪辑说明：{frame.get('editing_note', '')}",
                    ]
                )
            lines.append("")

        asset_preparation_notes = machine_payload_layer.get("asset_preparation_notes", [])
        if asset_preparation_notes:
            lines.append("### 结构化素材准备项")
            for item in asset_preparation_notes:
                lines.extend(
                    [
                        f"- 素材：{item.get('item_name', '')}",
                        f"  - 对应分镜：{item.get('linked_beat_number', '')}",
                        f"  - 要求：{item.get('requirement_detail', '')}",
                        f"  - 准备阶段：{item.get('ready_stage', '')}",
                    ]
                )
            lines.append("")

        voiceover_subtitle_alignment = machine_payload_layer.get("voiceover_subtitle_alignment", [])
        if voiceover_subtitle_alignment:
            lines.append("### 结构化配音字幕对齐")
            for item in voiceover_subtitle_alignment:
                lines.extend(
                    [
                        f"- 对应分镜：{item.get('linked_beat_number', '')}",
                        f"  - 配音：{item.get('voiceover_line', '')}",
                        f"  - 字幕：{item.get('subtitle_line', '')}",
                        f"  - 时序说明：{item.get('timing_note', '')}",
                    ]
                )
            lines.append("")

        self._append_candidate_lines(lines, "### 封面结构化候选", platform_layer.get("cover_candidates", []))
        self._append_candidate_lines(lines, "### 分发角度结构化候选", platform_layer.get("distribution_angle_candidates", []))
        self._append_detail_items(lines, "### 平台扩写：发布打法", platform_expansion.get("publishing_playbook", []))
        self._append_candidate_lines(lines, "### 平台扩写：评论线程打法", platform_expansion.get("comment_thread_playbook", []))
        self._append_detail_items(lines, "### 平台扩写：封面迭代说明", platform_expansion.get("cover_iteration_notes", []))
        self._append_candidate_lines(lines, "### 平台扩写：连载延展方向", platform_expansion.get("series_extension_angles", []))
        self._append_detail_items(lines, "### 平台扩写：发布时间节奏", platform_expansion.get("release_rhythm_notes", []))
        self._append_detail_items(lines, "### 多模态扩写：场景蓝图", multimodal_expansion.get("scene_blueprints", []))
        self._append_detail_items(lines, "### 多模态扩写：视觉母题", multimodal_expansion.get("visual_motif_notes", []))
        self._append_detail_items(lines, "### 多模态扩写：音频层次", multimodal_expansion.get("audio_layering_notes", []))
        self._append_detail_items(lines, "### 多模态扩写：素材管线", multimodal_expansion.get("asset_pipeline_notes", []))
        self._append_detail_items(lines, "### 机器扩写：制作阶段", machine_payload_expansion.get("production_phases", []))
        self._append_detail_items(lines, "### 机器扩写：字幕策略", machine_payload_expansion.get("subtitle_strategy_notes", []))
        self._append_detail_items(lines, "### 机器扩写：质检关卡", machine_payload_expansion.get("qa_checkpoints", []))
        if machine_payload_expansion.get("fallback_actions"):
            lines.extend(
                [
                    "### 机器扩写：失败回退动作",
                    f"- {' / '.join(machine_payload_expansion.get('fallback_actions', []))}",
                    "",
                ]
            )
        if machine_payload_layer.get("quality_control_notes"):
            lines.extend(
                [
                    "### 全局质控说明",
                    f"- {' / '.join(machine_payload_layer.get('quality_control_notes', []))}",
                    "",
                ]
            )

        return "\n".join(lines)

    def build_video_payload(self, result: ResultEnvelope) -> VideoGenerationPayload:
        request_summary = result.request_summary
        script_layer = result.result_package.script_layer
        multimodal_layer = result.result_package.multimodal_layer
        machine_payload_layer = result.result_package.machine_payload_layer
        overview = result.result_package.overview

        return VideoGenerationPayload(
            video_meta={
                "title": overview['main_title'],
                "platform": request_summary['target_platform'],
                "summary": overview['one_sentence_summary'],
            },
            segments=script_layer['segments'],
            shots=script_layer['key_shots'],
            characters=multimodal_layer['characters'],
            scenes=multimodal_layer['scenes'],
            scene_progression=multimodal_layer.get('scene_progression', []),
            motion_cues=multimodal_layer.get('motion_cues', []),
            asset_props=multimodal_layer.get('asset_props', []),
            visual_references=multimodal_layer.get('visual_references', []),
            style_constraints=machine_payload_layer['style_constraints'],
            subtitle_blocks=[segment['subtitle_text'] for segment in script_layer['segments']],
            audio_guides=multimodal_layer['audio_guides'],
            negative_constraints=machine_payload_layer['negative_constraints'],
            publish_timing_suggestions=result.result_package.platform_layer.get('publish_timing_suggestions', []),
            distribution_angles=result.result_package.platform_layer.get('distribution_angles', []),
            thumbnail_copy_candidates=result.result_package.platform_layer.get('thumbnail_copy_candidates', []),
            comment_guidance=result.result_package.platform_layer.get('comment_guidance', []),
            cover_copy_alternatives=result.result_package.platform_layer.get('cover_copy_alternatives', []),
            title_alternatives=script_layer.get('title_alternatives', []),
            hook_alternatives=script_layer.get('hook_alternatives', []),
            title_candidates=script_layer.get('title_candidates', []),
            hook_candidates=script_layer.get('hook_candidates', []),
            cover_candidates=result.result_package.platform_layer.get('cover_candidates', []),
            distribution_angle_candidates=result.result_package.platform_layer.get('distribution_angle_candidates', []),
            editing_checklist=machine_payload_layer.get('editing_checklist', []),
            cta_variants=machine_payload_layer.get('cta_variants', []),
            storyboard_beats=machine_payload_layer.get('storyboard_beats', []),
            storyboard_frames=machine_payload_layer.get('storyboard_frames', []),
            asset_preparation_notes=machine_payload_layer.get('asset_preparation_notes', []),
            voiceover_subtitle_alignment=machine_payload_layer.get('voiceover_subtitle_alignment', []),
            estimated_total_duration_seconds=machine_payload_layer.get('estimated_total_duration_seconds', 0),
            runtime_pacing_notes=machine_payload_layer.get('runtime_pacing_notes', []),
            trend_source_trace=result.analysis['trend_summary'].get('source_trace', []),
            overview_expansion=result.result_package.overview.get('expanded_breakdown', {}),
            analysis_expansion=result.analysis.get('expanded_analysis', {}),
            expanded_segments=script_layer.get('expanded_segments', []),
            expanded_key_shots=script_layer.get('expanded_key_shots', []),
            title_strategy_notes=script_layer.get('title_strategy_notes', []),
            hook_strategy_notes=script_layer.get('hook_strategy_notes', []),
            retention_design_notes=script_layer.get('retention_design_notes', []),
            multimodal_expansion=multimodal_layer.get('expanded_visual_plan', {}),
            platform_expansion=result.result_package.platform_layer.get('expanded_distribution_playbook', {}),
            machine_payload_expansion=machine_payload_layer.get('expanded_execution_plan', {}),
            quality_control_notes=machine_payload_layer.get('quality_control_notes', []),
        )


export_payload_service = ExportPayloadService()
