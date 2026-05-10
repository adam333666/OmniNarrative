from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class LiteLLMCompletionResult:
    content: str
    model: str


class LiteLLMUnavailableError(RuntimeError):
    pass


class LiteLLMTimeoutError(RuntimeError):
    pass


class LiteLLMResponseFormatError(RuntimeError):
    pass


class LiteLLMProviderError(RuntimeError):
    pass


class LiteLLMAdapter:
    def __init__(self) -> None:
        try:
            import litellm  # type: ignore
        except Exception as exc:  # pragma: no cover - depends on optional runtime dependency
            raise LiteLLMUnavailableError(str(exc)) from exc

        self._litellm = litellm

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
        try:
            response = self._litellm.completion(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=temperature,
                response_format=response_format,
                timeout=timeout,
            )
        except TimeoutError as exc:
            raise LiteLLMTimeoutError(str(exc) or "litellm completion timed out") from exc
        except Exception as exc:
            raise LiteLLMProviderError(str(exc) or "litellm provider call failed") from exc

        try:
            content = response["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise LiteLLMResponseFormatError("litellm response did not contain choices[0].message.content") from exc
        if not isinstance(content, str) or not content.strip():
            raise LiteLLMResponseFormatError("litellm response content was empty or non-string")
        return LiteLLMCompletionResult(content=content, model=model)
