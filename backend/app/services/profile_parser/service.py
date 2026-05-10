from __future__ import annotations

import logging

from app.schemas.creation_request import CreationRequest
from app.schemas.profiles import AudienceProfile, StyleProfile
from app.services.structured_output_gateway.service import (
    StructuredOutputGatewayService,
    structured_output_gateway_service,
)

logger = logging.getLogger(__name__)


class ProfileParserService:
    def __init__(
        self,
        structured_output_gateway: StructuredOutputGatewayService | None = None,
    ) -> None:
        self.structured_output_gateway = structured_output_gateway or structured_output_gateway_service

    def parse_audience_profile(self, request: CreationRequest) -> AudienceProfile:
        profile = self._parse_with_instructor(
            response_model=AudienceProfile,
            messages=self._build_audience_messages(request),
            fallback_factory=lambda: self._fallback_audience_profile(request),
        )
        return self._normalize_audience_profile(profile, request)

    def parse_style_profile(self, request: CreationRequest) -> StyleProfile:
        profile = self._parse_with_instructor(
            response_model=StyleProfile,
            messages=self._build_style_messages(request),
            fallback_factory=lambda: self._fallback_style_profile(request),
        )
        return self._normalize_style_profile(profile, request)

    def _parse_with_instructor(
        self,
        *,
        response_model: type[AudienceProfile] | type[StyleProfile],
        messages: list[dict[str, str]],
        fallback_factory,
    ) -> AudienceProfile | StyleProfile:
        result = self.structured_output_gateway.generate(
            caller_name="profile_parser",
            response_model=response_model,
            messages=messages,
        )
        if result is None:
            return fallback_factory()
        return result

    def _build_audience_messages(self, request: CreationRequest) -> list[dict[str, str]]:
        return [
            {
                "role": "system",
                "content": (
                    "你是短视频内容策划中的受众画像抽取器。"
                    "请严格依据给定信息，输出可被 Pydantic AudienceProfile 校验通过的结构化结果。"
                    "不要解释，不要输出 schema 之外的字段。"
                    "如果信息不足，请给出最合理且克制的推断。"
                ),
            },
            {
                "role": "user",
                "content": (
                    f"主题: {request.theme_text}\n"
                    f"内容类型: {request.content_type}\n"
                    f"目标平台: {request.target_platform}\n"
                    f"受众描述: {request.target_audience_text}\n"
                    "请抽取年龄段、兴趣标签、痛点、内容偏好与情绪偏好。"
                    "所有列表字段请使用简短中文短语。"
                ),
            },
        ]

    def _build_style_messages(self, request: CreationRequest) -> list[dict[str, str]]:
        custom_style_text = request.custom_style_text.strip() if request.custom_style_text else "无"
        return [
            {
                "role": "system",
                "content": (
                    "你是短视频内容风格抽取器。"
                    "请严格依据给定信息，输出可被 Pydantic StyleProfile 校验通过的结构化结果。"
                    "style_label 必须原样回填输入中的 style_tone。"
                    "intensity_level 只能是 low、medium、high。"
                    "不要解释，不要输出 schema 之外的字段。"
                ),
            },
            {
                "role": "user",
                "content": (
                    f"主题: {request.theme_text}\n"
                    f"目标平台: {request.target_platform}\n"
                    f"style_tone: {request.style_tone}\n"
                    f"自定义风格备注: {custom_style_text}\n"
                    "请抽取风格标签、情绪标签、强度等级与自定义备注。"
                ),
            },
        ]

    def _fallback_audience_profile(self, request: CreationRequest) -> AudienceProfile:
        audience_text = request.target_audience_text.strip()
        lowered = audience_text.lower()

        age_group_guess = "18-24"
        if any(token in audience_text for token in ["高中", "高三", "学生"]):
            age_group_guess = "16-20"
        elif any(token in audience_text for token in ["上班族", "职场", "白领"]):
            age_group_guess = "22-35"
        elif any(token in audience_text for token in ["家长", "父母"]):
            age_group_guess = "28-45"

        interest_tags = []
        if "科学" in audience_text or "科幻" in audience_text or "脑洞" in audience_text:
            interest_tags.append("脑洞设定")
        if "情绪" in audience_text or "焦虑" in audience_text:
            interest_tags.append("情绪共鸣")
        if "知识" in audience_text or "原理" in audience_text:
            interest_tags.append("知识增量")
        if not interest_tags:
            interest_tags.append("内容探索")

        pain_points = []
        if "焦虑" in audience_text:
            pain_points.append("情绪压力需要被理解")
        if "不会" in audience_text or "不懂" in audience_text:
            pain_points.append("复杂概念理解门槛高")
        if not pain_points:
            pain_points.append("需要更快进入内容主题")

        content_preference = ["开头要快", "结构要清楚"]
        if "b站" in lowered or "bilibili" in lowered:
            content_preference.append("愿意接受信息密度更高的表达")

        emotion_preference = ["希望被带入但不被说教"]

        return AudienceProfile(
            raw_text=audience_text,
            age_group_guess=age_group_guess,
            interest_tags=interest_tags,
            pain_points=pain_points,
            content_preference=content_preference,
            emotion_preference=emotion_preference,
        )

    def _fallback_style_profile(self, request: CreationRequest) -> StyleProfile:
        custom_notes = request.custom_style_text.strip() if request.custom_style_text else None
        intensity_level = "medium"
        if request.style_tone in {"high_emotion", "passionate", "twist"}:
            intensity_level = "high"
        elif request.style_tone in {"calm", "healing"}:
            intensity_level = "low"

        emotion_map = {
            "suspense": "紧张好奇",
            "healing": "柔和安定",
            "passionate": "强烈推进",
            "serious": "理性克制",
            "light": "轻快易进入",
            "twist": "意外反差",
            "high_emotion": "情绪浓度高",
            "calm": "稳定平缓",
            "inspirational": "鼓舞提振",
            "mysterious": "神秘探索",
        }

        return StyleProfile(
            style_label=request.style_tone,
            emotion_label=emotion_map.get(request.style_tone, "清晰表达"),
            intensity_level=intensity_level,
            custom_notes=custom_notes,
        )

    def _normalize_audience_profile(self, profile: AudienceProfile, request: CreationRequest) -> AudienceProfile:
        fallback = self._fallback_audience_profile(request)
        return AudienceProfile(
            raw_text=profile.raw_text.strip() or fallback.raw_text,
            age_group_guess=profile.age_group_guess.strip() or fallback.age_group_guess,
            interest_tags=self._coalesce_string_list(profile.interest_tags, fallback.interest_tags),
            pain_points=self._coalesce_string_list(profile.pain_points, fallback.pain_points),
            content_preference=self._coalesce_string_list(profile.content_preference, fallback.content_preference),
            emotion_preference=self._coalesce_string_list(profile.emotion_preference, fallback.emotion_preference),
        )

    def _normalize_style_profile(self, profile: StyleProfile, request: CreationRequest) -> StyleProfile:
        fallback = self._fallback_style_profile(request)
        custom_notes = profile.custom_notes.strip() if profile.custom_notes else None
        return StyleProfile(
            style_label=profile.style_label.strip() or fallback.style_label,
            emotion_label=profile.emotion_label.strip() or fallback.emotion_label,
            intensity_level=profile.intensity_level,
            custom_notes=custom_notes if custom_notes else fallback.custom_notes,
        )

    def _coalesce_string_list(self, values: list[str], fallback: list[str]) -> list[str]:
        cleaned = [item.strip() for item in values if item.strip()]
        return cleaned or list(fallback)


profile_parser_service = ProfileParserService()
