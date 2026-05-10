from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any

import httpx
from pydantic import ValidationError

from app.schemas.trend_template import SearchBackedTrendObservation


class AIHubMixSearchUnavailableError(RuntimeError):
    pass


class AIHubMixSearchProviderError(RuntimeError):
    pass


class AIHubMixSearchResponseFormatError(RuntimeError):
    pass


@dataclass(slots=True)
class AIHubMixSearchRequest:
    platform: str
    content_type: str
    baseline_summary: str
    baseline_hook_patterns: list[str]
    baseline_rhythm_patterns: list[str]
    baseline_title_cover_style: list[str]
    baseline_audience_preference_summary: str
    baseline_avoid_patterns: list[str]
    baseline_hot_topics_summary: list[str]
    baseline_interaction_patterns: list[str]
    baseline_emotional_entry_points: list[str]
    baseline_creator_angle_summary: str
    native_source_url: str | None = None
    native_source_title: str | None = None
    native_markdown_excerpt: str | None = None


class AIHubMixSearchAdapter:
    def __init__(
        self,
        *,
        api_key: str,
        base_url: str,
        model: str,
        timeout_seconds: float = 45.0,
        client: httpx.Client | None = None,
    ) -> None:
        if not api_key.strip():
            raise AIHubMixSearchUnavailableError("aihubmix api key is missing")
        if not base_url.strip():
            raise AIHubMixSearchUnavailableError("aihubmix base url is missing")
        if not model.strip():
            raise AIHubMixSearchUnavailableError("aihubmix search model is missing")

        self.api_key = api_key.strip()
        self.base_url = base_url.rstrip("/")
        self.model = model.strip()
        self.timeout_seconds = timeout_seconds
        self._client = client or httpx.Client(timeout=timeout_seconds)

    def generate_observation(self, request: AIHubMixSearchRequest) -> SearchBackedTrendObservation:
        system_prompt = (
            "你是中文短视频平台趋势研究员。"
            "你必须先使用 web search 获取近期公开网页信息，再结合给定的原生抓取摘要，"
            "输出一个严格合法的 JSON 对象。"
            "不要输出 markdown，不要输出解释，不要输出 JSON 之外的任何文字。"
            "JSON 必须包含以下字段："
            "summary, hook_patterns, rhythm_patterns, title_cover_style, audience_preference_summary, "
            "avoid_patterns, hot_topics_summary, interaction_patterns, emotional_entry_points, "
            "creator_angle_summary, source_trace。"
            "source_trace 必须是 2 到 4 条来源，每条包含 title, link, excerpt, source_name。"
            "所有短语使用简短、具体、可直接复用的中文。"
        )
        user_prompt = (
            f"平台: {request.platform}\n"
            f"内容类型: {request.content_type}\n"
            f"当前模板摘要: {request.baseline_summary}\n"
            f"当前钩子模式: {', '.join(request.baseline_hook_patterns)}\n"
            f"当前节奏模式: {', '.join(request.baseline_rhythm_patterns)}\n"
            f"当前标题封面风格: {', '.join(request.baseline_title_cover_style)}\n"
            f"当前受众偏好摘要: {request.baseline_audience_preference_summary}\n"
            f"当前避免模式: {', '.join(request.baseline_avoid_patterns)}\n"
            f"当前热点摘要: {', '.join(request.baseline_hot_topics_summary)}\n"
            f"当前互动模式: {', '.join(request.baseline_interaction_patterns)}\n"
            f"当前情绪切口: {', '.join(request.baseline_emotional_entry_points)}\n"
            f"当前创作者角度摘要: {request.baseline_creator_angle_summary}\n"
            f"原生抓取标题: {request.native_source_title or '无'}\n"
            f"原生抓取 URL: {request.native_source_url or '无'}\n"
            f"原生抓取摘要: {request.native_markdown_excerpt or '无'}\n"
            "请优先基于最近公开网页信息总结近期趋势；如果提供了原生抓取摘要，请把它作为补充证据。"
            "请输出适合当前平台与内容类型的趋势模板，不要机械重复基线。"
        )

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.2,
            "response_format": {"type": "json_object"},
            "web_search_options": {},
        }
        response = self._client.post(
            f"{self.base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
        )
        if response.status_code >= 400:
            raise AIHubMixSearchProviderError(response.text.strip() or f"provider error {response.status_code}")

        try:
            raw_payload = response.json()
            content = raw_payload["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise AIHubMixSearchResponseFormatError("response did not contain choices[0].message.content") from exc

        if not isinstance(content, str) or not content.strip():
            raise AIHubMixSearchResponseFormatError("response content was empty")

        try:
            parsed = json.loads(self._extract_json_object(content))
        except ValueError as exc:
            raise AIHubMixSearchResponseFormatError("response content was not valid json") from exc

        try:
            return SearchBackedTrendObservation.model_validate(self._normalize_payload(parsed, request))
        except ValidationError as exc:
            raise AIHubMixSearchResponseFormatError(str(exc)) from exc

    def _extract_json_object(self, content: str) -> str:
        stripped = content.strip()
        if stripped.startswith("```"):
            stripped = stripped.strip("`")
            if stripped.startswith("json"):
                stripped = stripped[4:]
            stripped = stripped.strip()
        if stripped.startswith("{") and stripped.endswith("}"):
            return stripped
        start = stripped.find("{")
        end = stripped.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise ValueError("json object boundaries not found")
        return stripped[start : end + 1]

    def _normalize_payload(self, payload: dict[str, Any], request: AIHubMixSearchRequest) -> dict[str, Any]:
        normalized = dict(payload)

        string_fallbacks = {
            "summary": request.baseline_summary,
            "audience_preference_summary": request.baseline_audience_preference_summary,
            "creator_angle_summary": request.baseline_creator_angle_summary,
        }
        list_fallbacks = {
            "hook_patterns": request.baseline_hook_patterns,
            "rhythm_patterns": request.baseline_rhythm_patterns,
            "title_cover_style": request.baseline_title_cover_style,
            "avoid_patterns": request.baseline_avoid_patterns,
            "hot_topics_summary": request.baseline_hot_topics_summary,
            "interaction_patterns": request.baseline_interaction_patterns,
            "emotional_entry_points": request.baseline_emotional_entry_points,
        }
        list_limits = {
            "hook_patterns": (2, 4),
            "rhythm_patterns": (2, 4),
            "title_cover_style": (2, 4),
            "avoid_patterns": (2, 4),
            "hot_topics_summary": (2, 5),
            "interaction_patterns": (2, 4),
            "emotional_entry_points": (2, 4),
        }

        for field, fallback in string_fallbacks.items():
            normalized[field] = self._normalize_string_field(normalized.get(field), fallback)

        for field, fallback in list_fallbacks.items():
            min_items, max_items = list_limits[field]
            normalized[field] = self._normalize_list_field(
                normalized.get(field),
                fallback,
                min_items=min_items,
                max_items=max_items,
            )

        return normalized

    def _normalize_string_field(self, value: Any, fallback: str) -> str:
        if isinstance(value, list):
            flattened = self._flatten_candidate_items(value)
            if flattened:
                return "；".join(flattened)
        if isinstance(value, str) and value.strip():
            return value.strip()
        return fallback.strip()

    def _normalize_list_field(
        self,
        value: Any,
        fallback: list[str],
        *,
        min_items: int,
        max_items: int,
    ) -> list[str]:
        normalized_items = self._flatten_candidate_items(value)
        fallback_items = self._flatten_candidate_items(fallback)

        merged_items: list[str] = []
        for item in [*normalized_items, *fallback_items]:
            if item not in merged_items:
                merged_items.append(item)

        if len(merged_items) < min_items:
            return fallback_items[:max_items]

        return merged_items[:max_items]

    def _flatten_candidate_items(self, value: Any) -> list[str]:
        if value is None:
            return []

        candidates: list[str] = []
        if isinstance(value, str):
            candidates = [value]
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, str):
                    candidates.append(item)
                elif item is not None:
                    candidates.append(str(item))
        else:
            candidates = [str(value)]

        normalized: list[str] = []
        for candidate in candidates:
            for item in self._split_phrase(candidate):
                if item not in normalized:
                    normalized.append(item)

        return normalized

    def _split_phrase(self, value: str) -> list[str]:
        text = value.strip()
        if not text:
            return []

        split_pattern = r"[、，,；;／/|]+|\s{2,}"
        parts = [part.strip(" \t\r\n-•1234567890.()[]【】") for part in re.split(split_pattern, text)]

        normalized = [part for part in parts if part]
        return normalized or [text]
