from __future__ import annotations

from app.schemas.creation_request import CreationRequest
from app.schemas.narrative_package import (
    AnalysisExpansion,
    ExpandedKeyShot,
    ExpandedPackageScaffold,
    ExpandedScriptSegment,
    ExpansionDetailItem,
    MachinePayloadExpansion,
    MultimodalExpansion,
    OverviewExpansion,
    PlatformExpansion,
    ScriptExpansion,
    StructuredTextCandidate,
)
from app.schemas.profiles import AudienceProfile, StyleProfile
from app.schemas.trend_template import PlatformTrendTemplate
from app.services.structured_output_gateway.service import (
    StructuredOutputGatewayService,
    structured_output_gateway_service,
)


class PackageExpanderService:
    def __init__(self, structured_output_gateway: StructuredOutputGatewayService | None = None) -> None:
        self.structured_output_gateway = structured_output_gateway or structured_output_gateway_service

    def build_expansion(
        self,
        *,
        request: CreationRequest,
        audience_profile: AudienceProfile,
        style_profile: StyleProfile,
        trend_summary: PlatformTrendTemplate,
        overview: dict,
        script_layer: dict,
        multimodal_layer: dict,
        platform_layer: dict,
        machine_payload_layer: dict,
    ) -> tuple[ExpandedPackageScaffold, dict[str, str | None]]:
        structured = None
        if not getattr(self.structured_output_gateway, "_uses_default_instructor_client_factory", False):
            try:
                structured = self.structured_output_gateway.generate(
                    caller_name="package_expander",
                    response_model=ExpandedPackageScaffold,
                    messages=self._build_structured_messages(
                        request=request,
                        audience_profile=audience_profile,
                        style_profile=style_profile,
                        trend_summary=trend_summary,
                        overview=overview,
                        script_layer=script_layer,
                        multimodal_layer=multimodal_layer,
                        platform_layer=platform_layer,
                        machine_payload_layer=machine_payload_layer,
                    ),
                )
            except Exception:
                structured = None
        if structured is not None:
            return structured, {
                "source_type": "structured_output_gateway",
                "fallback_reason": None,
            }

        return (
            self._build_fallback_expansion(
                request=request,
                audience_profile=audience_profile,
                style_profile=style_profile,
                trend_summary=trend_summary,
                overview=overview,
                script_layer=script_layer,
                multimodal_layer=multimodal_layer,
                platform_layer=platform_layer,
                machine_payload_layer=machine_payload_layer,
            ),
            {
                "source_type": "package_expander_fallback",
                "fallback_reason": "structured_output_skipped_or_failed",
            },
        )

    def _build_structured_messages(
        self,
        *,
        request: CreationRequest,
        audience_profile: AudienceProfile,
        style_profile: StyleProfile,
        trend_summary: PlatformTrendTemplate,
        overview: dict,
        script_layer: dict,
        multimodal_layer: dict,
        platform_layer: dict,
        machine_payload_layer: dict,
    ) -> list[dict[str, str]]:
        return [
            {
                "role": "system",
                "content": (
                    "你是结果包扩写器。"
                    "请严格输出可被 Pydantic ExpandedPackageScaffold 校验通过的结构化结果。"
                    "你的任务不是改写真值，而是在现有真值上做专业扩写，让每层都有更厚、更细、更可执行的说明。"
                    "不要重复粘贴完整原始需求文本，不要把长主题原文机械塞进封面文案、评论引导和分发角度。"
                    "所有扩写都要压缩成用户可直接使用的专业内容表达。"
                    "expanded_segments、expanded_key_shots、publishing_playbook、production_phases、qa_checkpoints 要尽量具体。"
                    "不要输出 schema 之外的字段。"
                ),
            },
            {
                "role": "user",
                "content": (
                    f"主题: {request.theme_text}\n"
                    f"内容类型: {request.content_type}\n"
                    f"目标平台: {request.target_platform}\n"
                    f"受众画像: {audience_profile.model_dump_json()}\n"
                    f"风格画像: {style_profile.model_dump_json()}\n"
                    f"趋势模板: {trend_summary.model_dump_json()}\n"
                    f"overview 真值: {overview}\n"
                    f"script_layer 真值: {script_layer}\n"
                    f"multimodal_layer 真值: {multimodal_layer}\n"
                    f"platform_layer 真值: {platform_layer}\n"
                    f"machine_payload_layer 真值: {machine_payload_layer}\n"
                    "请为每层补足专业扩写信息，保证内容厚、细、有结构，并能直接进入策划、剪辑、分发和下游机器消费。"
                ),
            },
        ]

    def _build_fallback_expansion(
        self,
        *,
        request: CreationRequest,
        audience_profile: AudienceProfile,
        style_profile: StyleProfile,
        trend_summary: PlatformTrendTemplate,
        overview: dict,
        script_layer: dict,
        multimodal_layer: dict,
        platform_layer: dict,
        machine_payload_layer: dict,
    ) -> ExpandedPackageScaffold:
        primary_interest = self._first_or(audience_profile.interest_tags, "认知脑洞")
        primary_pain = self._first_or(audience_profile.pain_points, "复杂概念理解门槛")
        expanded_segments = [
            ExpandedScriptSegment(
                segment_number=segment["segment_number"],
                narrative_function=segment["segment_goal"],
                expansion_goal=f"把“{segment['segment_title']}”扩成既能看懂又能继续讨论的段落。",
                transition_in="承接上一段情绪或问题，把观众注意力重新压回当前核心矛盾。",
                transition_out="在结尾留下一个更具体的判断或追问，让下一段自然接手。",
                audience_psychology=f"这一段主要服务“{primary_interest}”相关兴趣，同时缓解“{primary_pain}”的理解门槛。",
                detail_outline=[
                    f"先说明这段为什么必须出现，避免观众把“{segment['segment_title']}”当成跳步信息。",
                    "再给一个更接近日常经验的类比，降低抽象理解门槛。",
                    "最后用一句短判断收束，把评论区讨论点提前埋进去。",
                ],
                delivery_notes=[
                    f"旁白语气保持{style_profile.emotion_label}，但避免连续三句都在讲概念。",
                    "这一段至少出现一次“问题 -> 解释 -> 判断”的闭环。",
                    "字幕不要和旁白逐字重复，优先突出判断句。",
                ],
                alt_narration_lines=[
                    f"如果把这一步想通，后面的大部分争议其实都会自己收束。",
                    f"这段最重要的不是信息量，而是把“{segment['segment_title']}”真正讲成可讨论的问题。",
                    "你会发现，真正让人停下来的从来不是设定本身，而是设定逼出来的选择。",
                ],
                visual_layers=[
                    segment["visual_description"],
                    "叠加一层关系箭头或概念对照卡，帮助观众快速定位信息结构。",
                    "保留一个可单独切片的判断型画面，方便后续二次分发。",
                ],
            )
            for segment in script_layer.get("segments", [])
        ]

        expanded_key_shots = [
            ExpandedKeyShot(
                shot_title=shot["shot_title"],
                narrative_role=shot["shot_focus"],
                composition_notes="主画面要先给判断，再给细节，不要一开始就堆满解释信息。",
                motion_design=shot.get("camera_movement") or "镜头运动优先服务信息强调，避免无意义晃动。",
                asset_layers=[
                    shot.get("asset_dependency") or "基础信息卡一层",
                    "关系图或关键词字幕一层",
                    "结论强化字幕一层",
                ],
                edit_variants=[
                    "主版本保留完整解释节奏。",
                    "切片版本优先保留最强结论句和最强对比画面。",
                    "无真人版本保留信息卡和字幕驱动结构。",
                ],
                failure_fallback="如果素材不够，至少保留问题字卡、关系箭头和一条判断字幕，先保证信息闭环。",
            )
            for shot in script_layer.get("key_shots", [])
        ]

        short_theme = self._condense_theme(request.theme_text)
        return ExpandedPackageScaffold(
            overview_expansion=OverviewExpansion(
                positioning_rationale=[
                    self._detail(
                        "定位成立原因",
                        f"这条内容之所以适合做成 {request.target_platform} 的 {request.content_type}，是因为它同时具备强问题意识、可解释空间和评论区继续延展的余量。",
                        "帮助策划理解为什么这不是单点脑洞，而是可持续传播的主题。",
                        "首发时先把核心问题讲清，再把抽象概念拆成可感知的生活判断。",
                    ),
                    self._detail(
                        "用户价值",
                        f"观众看完后不只是知道“{short_theme}”是什么，而是能带走一个更完整的判断框架。",
                        "让内容从知识传递升级为认知整理。",
                        "每一段都要留下一个可以复述给别人听的判断句。",
                    ),
                ],
                audience_value_points=[
                    self._detail(
                        "理解收益",
                        f"把复杂设定压缩成更容易进入的解释路径，直接回应“{primary_pain}”。",
                        "降低跳出率。",
                        "优先把最难懂的概念换成关系、选择和后果三种日常语言。",
                    ),
                    self._detail(
                        "讨论收益",
                        "让观众在看完后立刻知道自己可以在评论区讨论什么，而不是只留下“好像很厉害”的模糊印象。",
                        "增强互动率。",
                        "每一段结尾都预埋一个可争论点。",
                    ),
                ],
                execution_priorities=[
                    self._detail("优先级一", "先保证问题清晰，再保证解释完整，最后再追求文采和氛围。"),
                    self._detail("优先级二", "先做主版本完整闭环，再从中拆出适合切片的结论句与高对比画面。"),
                ],
                risk_controls=[
                    self._detail("风险一", "不要把整条内容写成概念堆叠的讲义，否则会削弱观看连续性。"),
                    self._detail("风险二", "不要把标题、封面、评论引导都写成超长句，否则会损失发布可用性。"),
                ],
            ),
            analysis_expansion=AnalysisExpansion(
                audience_mindset_layers=[
                    self._detail("进入动机", "观众先被脑洞设问吸引，再决定要不要继续听解释。"),
                    self._detail("停留动机", "真正让人停留的不是设定名词，而是这些设定会不会反过来改变人生判断。"),
                ],
                comprehension_barriers=[
                    self._detail("抽象门槛", "如果连续抛术语，观众会迅速失去锚点。", "提醒解释顺序设计", "先给冲突，再给术语名。"),
                    self._detail("逻辑门槛", "如果没有中间桥接句，观众会听到名词但不知道它们之间如何相互制约。"),
                ],
                emotional_triggers=[
                    self._detail("认知冲突", "这类主题最强的情绪不是刺激，而是“原来我以为自由的地方可能并不自由”。"),
                    self._detail("个人代入", "只要把理论落到后悔、重来、选择这几个词，普通观众就会迅速代入。"),
                ],
                trend_application_notes=[
                    self._detail("平台趋势落点", "B 站当下更吃完整解释链和人格化判断，所以不能只做短结论堆叠。"),
                    self._detail("分发趋势落点", "主视频讲完整逻辑，切片只切最反常识的一句，不要切半截解释。"),
                ],
            ),
            script_expansion=ScriptExpansion(
                expanded_segments=expanded_segments,
                expanded_key_shots=expanded_key_shots,
                title_strategy_notes=[
                    self._detail("标题策略", "标题必须同时承接问题感和判断感，不能只剩抽象名词。"),
                    self._detail("标题测试", "主标题走哲学问题，副标题走设定拆解，利于双版本测试。"),
                ],
                hook_strategy_notes=[
                    self._detail("开场策略", "开场第一句必须让观众立即感觉到：这不是科幻设定介绍，而是和自己有关的判断题。"),
                    self._detail("开场节奏", "3 秒内要出现可复述的问题句，不能先做背景铺垫。"),
                ],
                retention_design_notes=[
                    self._detail("留存设计", "每段都要完成一次“小问题 -> 小解释 -> 小收束”，避免长段平铺。"),
                    self._detail("讨论设计", "在第 2 段和第 4 段故意留下两种互相冲突的解释空间，方便评论区分流讨论。"),
                ],
            ),
            multimodal_expansion=MultimodalExpansion(
                scene_blueprints=[
                    self._detail("开场场景", "开场必须优先给冲突感和时间异常感，不要先给背景世界观。"),
                    self._detail("解释场景", "解释段用关系图、对照卡、分叉线替代抽象口播，减轻理解负担。"),
                ],
                visual_motif_notes=[
                    self._detail("视觉母题", "反复使用时钟、分叉线、回卷箭头，让观众建立统一认知锚点。"),
                    self._detail("颜色策略", "开场和转折处用高对比色，解释段改成更稳定的中性信息色。"),
                ],
                audio_layering_notes=[
                    self._detail("配乐层次", "开场用不稳定节奏制造悬疑，中段弱化音乐给解释让路，结尾再轻微抬起情绪。"),
                    self._detail("停顿层次", "关键判断句前后必须留半拍，不要把所有句子说成同一速度。"),
                ],
                asset_pipeline_notes=[
                    self._detail("素材优先级", "先准备问题字卡和关系图，再准备装饰性氛围素材。"),
                    self._detail("切片兼容", "所有关键画面都要能被单独截成短切片，不依赖前文才能成立。"),
                ],
            ),
            platform_expansion=PlatformExpansion(
                publishing_playbook=[
                    self._detail("首发玩法", "首发版本优先保持完整解释链，不要为了快而把中段讲薄。"),
                    self._detail("二发玩法", "二发切片只保留最强结论和最强对比图，不重复主视频的大段解释。"),
                ],
                comment_thread_playbook=[
                    self._candidate("你更接受自洽时间线，还是多世界诠释？为什么？", "置顶评论一楼", "先让观众站队，再拉高讨论深度。"),
                    self._candidate("如果真的能回去一次，你最想改的会是什么？", "置顶评论二楼", "把抽象设定拉回个人经历。"),
                    self._candidate("你觉得真正可怕的是不能改过去，还是改了也只是换了一条分支？", "高赞回复追问", "继续扩大世界观分歧。"),
                ],
                cover_iteration_notes=[
                    self._detail("封面控制", "封面文字必须短，最多保留一个核心问题和一个结果词。"),
                    self._detail("封面测试", "第一版打哲学冲突，第二版打设定误解，第三版打人生代入。"),
                ],
                series_extension_angles=[
                    self._candidate("如果未来人已经来过，我们为什么没发现？", "同系列下一条", "沿着时间旅行继续扩成观察型问题。"),
                    self._candidate("平行宇宙最残酷的地方，不是无限可能，而是无限失去", "系列第二条", "把世界观转成情绪冲击。"),
                    self._candidate("电影里的时间旅行为什么总在偷换规则？", "系列第三条", "回到大众熟悉媒介做低门槛延展。"),
                ],
                release_rhythm_notes=[
                    self._detail("发布节奏", "主视频发布后 24 小时内补一条评论区高频问题回应，承接讨论热度。"),
                    self._detail("切片节奏", "主视频稳定后再放短切片，不要在首发前抢走完整内容的点击。"),
                ],
            ),
            machine_payload_expansion=MachinePayloadExpansion(
                production_phases=[
                    self._detail("阶段一", "先锁标题、问题句和 3 个核心判断，再进入画面设计。"),
                    self._detail("阶段二", "先做信息卡和关系图，再补氛围镜头，避免后期视觉空转。"),
                    self._detail("阶段三", "字幕、配音、画面必须三次交叉检查，保证判断句和重点句没有错位。"),
                ],
                shot_execution_notes=expanded_key_shots,
                subtitle_strategy_notes=[
                    self._detail("字幕主原则", "字幕只保留判断句和转折句，不要把整段旁白都搬上屏幕。"),
                    self._detail("字幕节奏", "每段至少要有一条能独立截图传播的字幕句。"),
                ],
                qa_checkpoints=[
                    self._detail("质检一", "前 3 秒是否已经把问题讲明白，而不是只营造氛围。"),
                    self._detail("质检二", "中段是否真的完成解释链，而不是只重复问题。"),
                    self._detail("质检三", "结尾是否留下讨论口，而不是草草停在结论。"),
                ],
                fallback_actions=[
                    "如果时长超标，优先删掉修辞句，不删解释闭环。",
                    "如果素材不足，保留关系图和判断字幕，弱化装饰性镜头。",
                    "如果评论引导过长，缩成二选一站队问题。",
                ],
            ),
            quality_control_notes=[
                "任何扩写都不能破坏原有标题、段落主旨和趋势结论的真值。",
                "所有候选文案都必须可发布，不允许把原始长需求直接原样复制进去。",
                "分镜、字幕、剪辑建议之间必须能互相对齐，不能各写各的。",
            ],
        )

    def _detail(
        self,
        title: str,
        detail: str,
        purpose: str = "",
        execution_hint: str = "",
    ) -> ExpansionDetailItem:
        return ExpansionDetailItem(
            title=title,
            detail=detail,
            purpose=purpose,
            execution_hint=execution_hint,
        )

    def _candidate(self, text: str, usage: str, reason: str) -> StructuredTextCandidate:
        return StructuredTextCandidate(
            candidate_text=text,
            usage_scenario=usage,
            design_reason=reason,
        )

    def _condense_theme(self, theme_text: str) -> str:
        condensed = theme_text.strip()
        if len(condensed) <= 32:
            return condensed
        return condensed[:32].rstrip("，,。；;：: ") + "..."

    def _first_or(self, values: list[str], fallback: str) -> str:
        for value in values:
            cleaned = value.strip()
            if cleaned:
                return cleaned
        return fallback


package_expander_service = PackageExpanderService()
