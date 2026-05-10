from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("DATABASE_URL", f"sqlite+pysqlite:///{Path('/tmp/multi_media_test.db')}")

from app.integrations.llm.litellm_adapter import (
    LiteLLMCompletionResult,
    LiteLLMProviderError,
    LiteLLMResponseFormatError,
    LiteLLMTimeoutError,
    LiteLLMUnavailableError,
)
from app.services.model_gateway.service import ModelGatewayService, NarrativeDraftRequest


class FakeLiteLLMAdapter:
    def __init__(self) -> None:
        pass

    def completion(
        self,
        *,
        model: str,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.4,
        response_format: dict | None = None,
        timeout: float | None = None,
    ) -> LiteLLMCompletionResult:
        return LiteLLMCompletionResult(content="模型已生成平台适配叙事草案。", model=model)


class MissingLiteLLMAdapter:
    def __init__(self) -> None:
        raise LiteLLMUnavailableError("litellm is unavailable")


class BrokenLiteLLMAdapter:
    def __init__(self) -> None:
        pass

    def completion(
        self,
        *,
        model: str,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.4,
        response_format: dict | None = None,
        timeout: float | None = None,
    ) -> LiteLLMCompletionResult:
        raise LiteLLMProviderError("provider timeout")


class RetryThenSuccessAdapter:
    calls = 0

    def __init__(self) -> None:
        pass

    def completion(
        self,
        *,
        model: str,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.4,
        response_format: dict | None = None,
        timeout: float | None = None,
    ) -> LiteLLMCompletionResult:
        type(self).calls += 1
        if type(self).calls == 1:
            raise LiteLLMTimeoutError("provider timed out once")
        return LiteLLMCompletionResult(content="第二次尝试成功返回。", model=model)


class MalformedResponseAdapter:
    def __init__(self) -> None:
        pass

    def completion(
        self,
        *,
        model: str,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.4,
        response_format: dict | None = None,
        timeout: float | None = None,
    ) -> LiteLLMCompletionResult:
        raise LiteLLMResponseFormatError("missing content")


REQUEST = NarrativeDraftRequest(
    theme_text="时间旅行悖论",
    target_platform="bilibili",
    audience_summary="喜欢科幻与逻辑推理的年轻观众",
    style_summary="悬疑且有解释欲",
    trend_summary="设问推进、知识密度和完整解释链条。",
)


def test_model_gateway_uses_adapter_when_available() -> None:
    service = ModelGatewayService(adapter_factory=FakeLiteLLMAdapter, default_model="mock/model")

    response = service.generate_narrative_draft(REQUEST)

    assert response.source_type == "model_gateway_litellm"
    assert response.model_name == "mock/model"
    assert response.fallback_reason is None
    assert response.attempt_count == 1
    assert "模型已生成" in response.content


def test_model_gateway_falls_back_when_litellm_is_unavailable() -> None:
    service = ModelGatewayService(adapter_factory=MissingLiteLLMAdapter)

    response = service.generate_narrative_draft(REQUEST)

    assert response.source_type == "model_gateway_fallback"
    assert response.model_name is None
    assert response.fallback_reason == "provider_unavailable"
    assert response.attempt_count == 0
    assert "时间旅行悖论" in response.content
    assert "bilibili" in response.content


def test_model_gateway_falls_back_when_completion_call_fails() -> None:
    service = ModelGatewayService(adapter_factory=BrokenLiteLLMAdapter)

    response = service.generate_narrative_draft(REQUEST)

    assert response.source_type == "model_gateway_fallback"
    assert response.model_name is None
    assert response.fallback_reason == "provider_error"
    assert response.attempt_count == 2
    assert "时间旅行悖论" in response.content


def test_model_gateway_retries_timeout_and_uses_second_success() -> None:
    RetryThenSuccessAdapter.calls = 0
    service = ModelGatewayService(adapter_factory=RetryThenSuccessAdapter, default_model="mock/model", max_retries=1)

    response = service.generate_narrative_draft(REQUEST)

    assert response.source_type == "model_gateway_litellm"
    assert response.model_name == "mock/model"
    assert response.fallback_reason is None
    assert response.attempt_count == 2
    assert response.content == "第二次尝试成功返回。"


def test_model_gateway_marks_malformed_response_without_retry_looping() -> None:
    service = ModelGatewayService(adapter_factory=MalformedResponseAdapter, max_retries=3)

    response = service.generate_narrative_draft(REQUEST)

    assert response.source_type == "model_gateway_fallback"
    assert response.model_name is None
    assert response.fallback_reason == "malformed_response"
    assert response.attempt_count == 1


def test_model_gateway_falls_back_when_provider_config_is_missing() -> None:
    service = ModelGatewayService(adapter_factory=FakeLiteLLMAdapter, provider_name="disabled")

    response = service.generate_narrative_draft(REQUEST)

    assert response.source_type == "model_gateway_fallback"
    assert response.model_name is None
    assert response.fallback_reason == "provider_config_missing"
    assert response.attempt_count == 0
