from __future__ import annotations

import logging
from dataclasses import dataclass, field

from app.schemas.creation_request import CreationRequest
from app.schemas.narrative_generation import StructuredNarrativeBundle
from app.schemas.narrative_package import KeyShot, ScriptSegment, StructuredTextCandidate
from app.schemas.profiles import AudienceProfile, StyleProfile
from app.schemas.trend_template import PlatformTrendTemplate
from app.services.structured_output_gateway.service import (
    StructuredOutputGatewayService,
    structured_output_gateway_service,
)

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class NarrativeGenerationRuntime:
    source_type: str
    fallback_reason: str | None = None


@dataclass(slots=True)
class NarrativeBundleResult:
    title: str
    one_sentence_summary: str
    segments: list[ScriptSegment]
    key_shots: list[KeyShot]
    title_alternatives: list[str]
    hook_alternatives: list[str]
    runtime: NarrativeGenerationRuntime
    title_candidates: list[StructuredTextCandidate] = field(default_factory=list)
    hook_candidates: list[StructuredTextCandidate] = field(default_factory=list)


class NarrativeGeneratorService:
    def __init__(
        self,
        structured_output_gateway: StructuredOutputGatewayService | None = None,
    ) -> None:
        self.structured_output_gateway = structured_output_gateway or structured_output_gateway_service

    def build_main_title(self, request: CreationRequest, trend_summary: PlatformTrendTemplate) -> str:
        if request.target_platform == "bilibili":
            return f"{request.theme_text}，为什么会让人越想越上头？"
        if request.target_platform == "xiaohongshu":
            return f"关于{request.theme_text}，我终于找到一个更好讲清的方法"
        return f"{request.theme_text}，你可能一直都想错了"

    def build_one_sentence_summary(
        self,
        request: CreationRequest,
        audience_profile: AudienceProfile,
        style_profile: StyleProfile,
    ) -> str:
        return (
            f"围绕“{request.theme_text}”，用{style_profile.emotion_label}的表达方式，"
            f"面向{audience_profile.age_group_guess}人群完成一条兼顾理解与传播的内容方案。"
        )

    def build_segments(
        self,
        request: CreationRequest,
        audience_profile: AudienceProfile,
        style_profile: StyleProfile,
        trend_summary: PlatformTrendTemplate,
    ) -> tuple[
        list[ScriptSegment],
        list[KeyShot],
        list[str],
        list[str],
        list[StructuredTextCandidate],
        list[StructuredTextCandidate],
    ]:
        segments = [
            ScriptSegment(
                segment_number=1,
                segment_title="开头钩子",
                segment_goal="用平台适配的开场方式抓住注意力。",
                narration=f"先抛出一个关于“{request.theme_text}”的反常识问题，让观众立即进入情境。",
                subtitle_text=f"你以为你理解了{request.theme_text}，但真正的矛盾点其实刚刚开始。",
                visual_description="快速切换问题画面与核心概念关键词，形成第一眼冲击。",
                emotion=style_profile.emotion_label,
                rhythm=trend_summary.rhythm_patterns[0],
            ),
            ScriptSegment(
                segment_number=2,
                segment_title="问题展开",
                segment_goal="解释主题为什么与目标受众有关。",
                narration=f"把{request.theme_text}拆成观众最容易理解的两个切面，并指出它与现实感受的连接。",
                subtitle_text="它不只是一个话题，而是你早就碰到却没说清的那个困惑。",
                visual_description="通过一组由近到远的画面，把抽象话题落到具体感受上。",
                emotion=style_profile.emotion_label,
                rhythm="信息层层推进",
            ),
            ScriptSegment(
                segment_number=3,
                segment_title="核心解释",
                segment_goal="给出完整叙事主干和平台化表达。",
                narration=(
                    f"结合{audience_profile.interest_tags[0]}和平台节奏，给出一个可传播、可复述的核心解释框架。"
                ),
                subtitle_text="你真正会记住的，不是结论，而是这个被拆开的理解路径。",
                visual_description="主视觉进入稳定叙事段，用图形、关键词和人物反应强化理解。",
                emotion=style_profile.emotion_label,
                rhythm=trend_summary.rhythm_patterns[-1],
            ),
            ScriptSegment(
                segment_number=4,
                segment_title="收束与余味",
                segment_goal="把观点收束成可分享的结尾。",
                narration="最后把这条内容收束成一句值得评论区继续讨论的结尾判断。",
                subtitle_text="真正让人停下来想的，往往不是答案，而是答案背后的那一步转弯。",
                visual_description="镜头节奏放慢，用一句结尾问题或判断做余味停顿。",
                emotion=style_profile.emotion_label,
                rhythm="节奏收束并留下停顿",
            ),
        ]

        key_shots = [
            KeyShot(
                shot_title="钩子镜头",
                shot_focus="第一句反常识判断",
                shot_duration_seconds=4,
                transition_hint="直接切入核心问题",
                camera_movement="开场快速推近并轻微抖动停顿",
                transition_style="硬切进入问题字幕",
                asset_dependency="高对比问题字卡 + 主题关键词动效",
                voiceover_cue="第一句要压缩语速，问题词做重音停顿",
            ),
            KeyShot(
                shot_title="解释镜头",
                shot_focus="主题与受众关系的桥接",
                shot_duration_seconds=6,
                transition_hint="从疑问转入说明",
                camera_movement="从近景平移到信息卡中景",
                transition_style="问题字幕淡出后接解释信息卡",
                asset_dependency="关系图示卡 + 受众场景素材",
                voiceover_cue="解释句按两拍拆开，让字幕跟住转折点",
            ),
            KeyShot(
                shot_title="结尾镜头",
                shot_focus="可评论、可转发的结尾判断",
                shot_duration_seconds=5,
                transition_hint="以留白结束",
                camera_movement="镜头轻微拉远并停留结尾字幕",
                transition_style="解释段减速后溶解进结尾留白",
                asset_dependency="结尾提问字幕 + 评论引导卡",
                voiceover_cue="结尾判断句放慢半拍，最后一句单独留白",
            ),
        ]

        title_alternatives = [
            self.build_main_title(request, trend_summary),
            f"如果你也想讲清{request.theme_text}，这条结构更容易被记住",
            f"{request.theme_text}真正打动人的，不只是内容本身",
        ]
        hook_alternatives = [
            trend_summary.hook_patterns[0],
            trend_summary.hook_patterns[-1],
            f"先别急着下结论，{request.theme_text}真正有意思的是第二层。",
        ]

        title_candidates = self._build_candidates(
            title_alternatives,
            usage_scenarios=[
                "主发布标题",
                "封面主文案联动版本",
                "二次分发测试版本",
            ],
            design_reasons=[
                "优先承接当前平台主标题表达，保证首发版本稳定。",
                "强调封面与标题联动，便于封面测试时直接替换。",
                "保留一个更适合评论区、合集页或切片复用的版本。",
            ],
        )
        hook_candidates = self._build_candidates(
            hook_alternatives,
            usage_scenarios=[
                "正片前 3 秒开场",
                "口播起手版本",
                "切片复用版本",
            ],
            design_reasons=[
                "优先贴合平台钩子模式，保证开头抓人。",
                "适合讲述者直接口播起手，减少表演负担。",
                "为后续短切片或二次剪辑保留独立开场语。",
            ],
        )

        return segments, key_shots, title_alternatives, hook_alternatives, title_candidates, hook_candidates

    def _build_structured_messages(
        self,
        request: CreationRequest,
        audience_profile: AudienceProfile,
        style_profile: StyleProfile,
        trend_summary: PlatformTrendTemplate,
    ) -> list[dict[str, str]]:
        return [
            {
                "role": "system",
                "content": (
                    "你是短视频内容策划中的结构化脚本生成器。"
                    "请严格输出可被 Pydantic StructuredNarrativeBundle 校验通过的结果。"
                    "所有文案使用简洁、可执行的中文。"
                    "请确保 segments 至少 3 段，key_shots 至少 2 个。"
                    "title_candidates 与 hook_candidates 需要输出结构化候选，不要只返回裸字符串。"
                    "key_shots 需要尽量补全 camera_movement、transition_style、asset_dependency、voiceover_cue。"
                    "不要解释，不要输出 schema 之外的字段。"
                ),
            },
            {
                "role": "user",
                "content": (
                    f"主题: {request.theme_text}\n"
                    f"内容类型: {request.content_type}\n"
                    f"目标平台: {request.target_platform}\n"
                    f"受众原文: {audience_profile.raw_text}\n"
                    f"受众年龄猜测: {audience_profile.age_group_guess}\n"
                    f"受众兴趣: {', '.join(audience_profile.interest_tags)}\n"
                    f"受众痛点: {', '.join(audience_profile.pain_points)}\n"
                    f"内容偏好: {', '.join(audience_profile.content_preference)}\n"
                    f"情绪偏好: {', '.join(audience_profile.emotion_preference)}\n"
                    f"风格标签: {style_profile.style_label}\n"
                    f"核心情绪: {style_profile.emotion_label}\n"
                    f"风格强度: {style_profile.intensity_level}\n"
                    f"风格备注: {style_profile.custom_notes or '无'}\n"
                    f"趋势摘要: {trend_summary.summary}\n"
                    f"平台钩子模式: {', '.join(trend_summary.hook_patterns)}\n"
                    f"平台节奏模式: {', '.join(trend_summary.rhythm_patterns)}\n"
                    f"标题封面风格: {', '.join(trend_summary.title_cover_style)}\n"
                    f"避免模式: {', '.join(trend_summary.avoid_patterns)}\n"
                    "请生成适合该平台的重结构化内容方案，包含标题、一句话摘要、分段脚本、关键镜头、标题备选、开场钩子备选，以及对应的结构化候选层。"
                ),
            },
        ]

    def _build_structured_bundle(
        self,
        request: CreationRequest,
        audience_profile: AudienceProfile,
        style_profile: StyleProfile,
        trend_summary: PlatformTrendTemplate,
    ) -> StructuredNarrativeBundle | None:
        return self.structured_output_gateway.generate(
            caller_name="narrative_generator",
            response_model=StructuredNarrativeBundle,
            messages=self._build_structured_messages(request, audience_profile, style_profile, trend_summary),
        )

    def build_narrative_bundle_result(
        self,
        request: CreationRequest,
        audience_profile: AudienceProfile,
        style_profile: StyleProfile,
        trend_summary: PlatformTrendTemplate,
    ) -> NarrativeBundleResult:
        audience_profile = self._normalize_audience_profile(audience_profile)
        trend_summary = self._normalize_trend_summary(trend_summary)
        fallback_title = self.build_main_title(request, trend_summary)
        fallback_summary = self.build_one_sentence_summary(request, audience_profile, style_profile)
        (
            segments,
            key_shots,
            fallback_title_alternatives,
            hook_alternatives,
            fallback_title_candidates,
            fallback_hook_candidates,
        ) = self.build_segments(
            request,
            audience_profile,
            style_profile,
            trend_summary,
        )

        structured_bundle = self._build_structured_bundle(request, audience_profile, style_profile, trend_summary)
        if structured_bundle is not None:
            title_alternatives = self._merge_title_alternatives(
                generated_title=structured_bundle.main_title,
                generated_summary=structured_bundle.one_sentence_summary,
                fallback_title_alternatives=structured_bundle.title_alternatives,
            )
            hook_alternatives = self._merge_string_alternatives(
                generated_values=structured_bundle.hook_alternatives,
                fallback_values=hook_alternatives,
            )
            title_candidates = self._merge_candidate_lists(
                structured_candidates=structured_bundle.title_candidates,
                fallback_candidates=fallback_title_candidates,
                fallback_values=title_alternatives,
                usage_scenarios=["主发布标题", "封面主文案联动版本", "二次分发测试版本"],
                design_reasons=[
                    "优先保留结构化主标题候选，服务正式发布。",
                    "补一个更适合封面联动的标题版本。",
                    "补一个更适合分发测试的标题版本。",
                ],
            )
            hook_candidates = self._merge_candidate_lists(
                structured_candidates=structured_bundle.hook_candidates,
                fallback_candidates=fallback_hook_candidates,
                fallback_values=hook_alternatives,
                usage_scenarios=["正片前 3 秒开场", "口播起手版本", "切片复用版本"],
                design_reasons=[
                    "优先保留结构化开场候选，服务正式正片。",
                    "补一个更适合口播起手的版本。",
                    "补一个更适合切片复用的版本。",
                ],
            )
            return NarrativeBundleResult(
                title=structured_bundle.main_title,
                one_sentence_summary=structured_bundle.one_sentence_summary,
                segments=structured_bundle.segments,
                key_shots=structured_bundle.key_shots,
                title_alternatives=title_alternatives,
                hook_alternatives=hook_alternatives,
                title_candidates=title_candidates,
                hook_candidates=hook_candidates,
                runtime=NarrativeGenerationRuntime(source_type="structured_output_gateway", fallback_reason=None),
            )

        title_alternatives = self._merge_title_alternatives(
            generated_title=fallback_title,
            generated_summary=fallback_summary,
            fallback_title_alternatives=fallback_title_alternatives,
        )
        return NarrativeBundleResult(
            title=fallback_title,
            one_sentence_summary=fallback_summary,
            segments=segments,
            key_shots=key_shots,
            title_alternatives=title_alternatives,
            hook_alternatives=hook_alternatives,
            title_candidates=fallback_title_candidates,
            hook_candidates=fallback_hook_candidates,
            runtime=NarrativeGenerationRuntime(
                source_type="narrative_generator_fallback",
                fallback_reason="structured_output_unavailable_or_failed",
            ),
        )

    def _normalize_audience_profile(self, audience_profile: AudienceProfile) -> AudienceProfile:
        return audience_profile.model_copy(
            update={
                "interest_tags": self._coalesce_string_list(audience_profile.interest_tags, ["内容探索"]),
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

    def build_narrative_bundle(
        self,
        request: CreationRequest,
        audience_profile: AudienceProfile,
        style_profile: StyleProfile,
        trend_summary: PlatformTrendTemplate,
    ) -> tuple[str, str, list[ScriptSegment], list[KeyShot], list[str], list[str]]:
        result = self.build_narrative_bundle_result(request, audience_profile, style_profile, trend_summary)
        return (
            result.title,
            result.one_sentence_summary,
            result.segments,
            result.key_shots,
            result.title_alternatives,
            result.hook_alternatives,
        )

    def _merge_title_alternatives(
        self,
        generated_title: str,
        generated_summary: str,
        fallback_title_alternatives: list[str],
    ) -> list[str]:
        merged = [generated_title, generated_summary[:36], *fallback_title_alternatives]
        deduped: list[str] = []
        for item in merged:
            item = item.strip()
            if not item or item in deduped:
                continue
            deduped.append(item)
        return deduped[:3]

    def _merge_string_alternatives(self, generated_values: list[str], fallback_values: list[str]) -> list[str]:
        merged = [*generated_values, *fallback_values]
        deduped: list[str] = []
        for item in merged:
            item = item.strip()
            if not item or item in deduped:
                continue
            deduped.append(item)
        return deduped[:3]

    def _build_candidates(
        self,
        values: list[str],
        *,
        usage_scenarios: list[str],
        design_reasons: list[str],
    ) -> list[StructuredTextCandidate]:
        candidates: list[StructuredTextCandidate] = []
        for index, value in enumerate(values[:3]):
            cleaned = value.strip()
            if not cleaned:
                continue
            candidates.append(
                StructuredTextCandidate(
                    candidate_text=cleaned,
                    usage_scenario=usage_scenarios[min(index, len(usage_scenarios) - 1)],
                    design_reason=design_reasons[min(index, len(design_reasons) - 1)],
                )
            )
        return candidates

    def _merge_candidate_lists(
        self,
        *,
        structured_candidates: list[StructuredTextCandidate],
        fallback_candidates: list[StructuredTextCandidate],
        fallback_values: list[str],
        usage_scenarios: list[str],
        design_reasons: list[str],
    ) -> list[StructuredTextCandidate]:
        merged: list[StructuredTextCandidate] = []
        seen: set[str] = set()
        for candidate in [*structured_candidates, *fallback_candidates]:
            text = candidate.candidate_text.strip()
            if not text or text in seen:
                continue
            merged.append(candidate)
            seen.add(text)
        for candidate in self._build_candidates(
            fallback_values,
            usage_scenarios=usage_scenarios,
            design_reasons=design_reasons,
        ):
            text = candidate.candidate_text.strip()
            if not text or text in seen:
                continue
            merged.append(candidate)
            seen.add(text)
        return merged[:3]

    def _coalesce_string_list(self, values: list[str], fallback: list[str]) -> list[str]:
        cleaned = [item.strip() for item in values if item.strip()]
        return cleaned or list(fallback)


narrative_generator_service = NarrativeGeneratorService()
