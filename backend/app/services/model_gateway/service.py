from __future__ import annotations

import logging
from dataclasses import dataclass
from time import perf_counter

from app.core.config import settings

from app.integrations.llm.litellm_adapter import (
    LiteLLMAdapter,
    LiteLLMCompletionResult,
    LiteLLMProviderError,
    LiteLLMResponseFormatError,
    LiteLLMTimeoutError,
    LiteLLMUnavailableError,
)

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class NarrativeDraftRequest:
    theme_text: str
    target_platform: str
    audience_summary: str
    style_summary: str
    trend_summary: str


@dataclass(slots=True)
class NarrativeDraftResponse:
    content: str
    source_type: str
    model_name: str | None
    fallback_reason: str | None = None
    attempt_count: int = 0


class ModelGatewayService:
    def __init__(
        self,
        adapter_factory: type[LiteLLMAdapter] = LiteLLMAdapter,
        default_model: str | None = None,
        provider_name: str | None = None,
        timeout_seconds: float | None = None,
        max_retries: int | None = None,
        temperature: float | None = None,
    ) -> None:
        self.adapter_factory = adapter_factory
        self.provider_name = provider_name or settings.model_provider
        self.default_model = default_model or settings.model_name
        self.timeout_seconds = settings.model_timeout_seconds if timeout_seconds is None else timeout_seconds
        self.max_retries = settings.model_max_retries if max_retries is None else max_retries
        self.temperature = settings.model_temperature if temperature is None else temperature

    def generate_narrative_draft(self, request: NarrativeDraftRequest) -> NarrativeDraftResponse:
        if self.provider_name != "litellm":
            return self._build_fallback_response(request, reason="provider_config_missing", attempt_count=0)
        if not self.default_model.strip():
            return self._build_fallback_response(request, reason="provider_config_missing", attempt_count=0)

        try:
            adapter = self.adapter_factory()
        except LiteLLMUnavailableError:
            return self._build_fallback_response(request, reason="provider_unavailable", attempt_count=0)

        attempt_count = 0
        last_error_type = "provider_error"
        while attempt_count <= self.max_retries:
            attempt_count += 1
            started_at = perf_counter()
            try:
                result = self._run_completion(adapter=adapter, request=request)
            except LiteLLMTimeoutError:
                last_error_type = "timeout"
                self._log_attempt_failure(last_error_type, attempt_count, started_at)
                continue
            except LiteLLMResponseFormatError:
                last_error_type = "malformed_response"
                self._log_attempt_failure(last_error_type, attempt_count, started_at)
                break
            except LiteLLMProviderError:
                last_error_type = "provider_error"
                self._log_attempt_failure(last_error_type, attempt_count, started_at)
                continue
            else:
                elapsed_ms = (perf_counter() - started_at) * 1000
                logger.info(
                    "model_gateway completion succeeded provider=%s model=%s attempt=%s elapsed_ms=%.2f",
                    self.provider_name,
                    self.default_model,
                    attempt_count,
                    elapsed_ms,
                )
                return NarrativeDraftResponse(
                    content=result.content,
                    source_type="model_gateway_litellm",
                    model_name=result.model,
                    attempt_count=attempt_count,
                )
        return self._build_fallback_response(request, reason=last_error_type, attempt_count=attempt_count)

    def _run_completion(self, adapter: LiteLLMAdapter, request: NarrativeDraftRequest) -> LiteLLMCompletionResult:
        system_prompt = (
            "You are a structured narrative planner. "
            "Return a concise narrative draft that reflects platform, audience, style, and trend constraints."
        )
        user_prompt = (
            f"主题: {request.theme_text}\n"
            f"目标平台: {request.target_platform}\n"
            f"受众摘要: {request.audience_summary}\n"
            f"风格摘要: {request.style_summary}\n"
            f"趋势摘要: {request.trend_summary}\n"
            "请输出一段简洁的叙事草案，强调平台适配与传播钩子。"
        )
        return adapter.completion(
            model=self.default_model,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=self.temperature,
            timeout=self.timeout_seconds,
        )

    def _build_fallback_response(
        self,
        request: NarrativeDraftRequest,
        *,
        reason: str,
        attempt_count: int,
    ) -> NarrativeDraftResponse:
        logger.warning(
            "model_gateway fallback provider=%s model=%s reason=%s attempts=%s",
            self.provider_name,
            self.default_model,
            reason,
            attempt_count,
        )
        return NarrativeDraftResponse(
            content=self._build_fallback_content(request),
            source_type="model_gateway_fallback",
            model_name=None,
            fallback_reason=reason,
            attempt_count=attempt_count,
        )

    def _log_attempt_failure(self, error_type: str, attempt_count: int, started_at: float) -> None:
        elapsed_ms = (perf_counter() - started_at) * 1000
        logger.warning(
            "model_gateway attempt failed provider=%s model=%s error_type=%s attempt=%s elapsed_ms=%.2f",
            self.provider_name,
            self.default_model,
            error_type,
            attempt_count,
            elapsed_ms,
        )

    def _build_fallback_content(self, request: NarrativeDraftRequest) -> str:
        return (
            f"围绕{request.theme_text}，面向{request.target_platform}平台，"
            f"用{request.style_summary}的表达方式，先抓住{request.audience_summary}的兴趣，"
            f"并结合趋势要点“{request.trend_summary}”快速建立叙事钩子。"
        )


model_gateway_service = ModelGatewayService()
