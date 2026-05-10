from __future__ import annotations

import logging
import os
from collections.abc import Callable
from typing import Any, TypeVar

from app.core.config import settings

logger = logging.getLogger(__name__)

T = TypeVar("T")


class StructuredOutputGatewayService:
    def __init__(
        self,
        instructor_client_factory: Callable[[], Any] | None = None,
        provider_name: str | None = None,
        model_name: str | None = None,
        max_retries: int | None = None,
        temperature: float | None = None,
        timeout_seconds: float | None = None,
    ) -> None:
        self.instructor_client_factory = instructor_client_factory or self._default_instructor_client_factory
        self._uses_default_instructor_client_factory = instructor_client_factory is None
        self.provider_name = provider_name or settings.model_provider
        self.model_name = model_name or settings.model_name
        self.max_retries = settings.model_max_retries if max_retries is None else max_retries
        self.temperature = settings.model_temperature if temperature is None else temperature
        self.timeout_seconds = settings.model_timeout_seconds if timeout_seconds is None else timeout_seconds

    def _default_instructor_client_factory(self) -> Any:
        import instructor
        from litellm import completion

        return instructor.from_litellm(completion)

    def generate(
        self,
        *,
        caller_name: str,
        response_model: type[T],
        messages: list[dict[str, str]],
    ) -> T | None:
        if self.provider_name != "litellm":
            logger.info("%s fallback reason=unsupported_provider provider=%s", caller_name, self.provider_name)
            return None
        if not self.model_name.strip():
            logger.info("%s fallback reason=model_missing", caller_name)
            return None
        if self._uses_default_instructor_client_factory and not self._has_provider_credentials():
            logger.info("%s fallback reason=provider_credentials_missing model=%s", caller_name, self.model_name)
            return None

        try:
            client = self.instructor_client_factory()
        except Exception as exc:
            logger.warning("%s fallback reason=client_unavailable error=%s", caller_name, exc)
            return None

        try:
            result = client.create(
                response_model=response_model,
                messages=messages,
                model=self.model_name,
                max_retries=self.max_retries,
                temperature=self.temperature,
                timeout=self.timeout_seconds,
            )
        except Exception as exc:
            logger.warning("%s fallback reason=structured_extract_failed error=%s", caller_name, exc)
            return None

        return result if isinstance(result, response_model) else response_model.model_validate(result)

    def _has_provider_credentials(self) -> bool:
        provider_hint = self.model_name.split("/", 1)[0].strip().lower()

        if provider_hint == "openai":
            return bool(os.getenv("OPENAI_API_KEY", "").strip())
        if provider_hint == "anthropic":
            return bool(os.getenv("ANTHROPIC_API_KEY", "").strip() or os.getenv("ANTHROPIC_AUTH_TOKEN", "").strip())
        if provider_hint in {"google", "gemini"}:
            return bool(os.getenv("GOOGLE_API_KEY", "").strip() or os.getenv("GEMINI_API_KEY", "").strip())
        if provider_hint == "azure":
            return bool(os.getenv("AZURE_OPENAI_API_KEY", "").strip())
        return True


structured_output_gateway_service = StructuredOutputGatewayService()
