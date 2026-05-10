from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("DATABASE_URL", f"sqlite+pysqlite:///{Path('/tmp/multi_media_test.db')}")

from pydantic import BaseModel

from app.services.structured_output_gateway.service import StructuredOutputGatewayService


class DemoPayload(BaseModel):
    value: str


class FakeInstructorClient:
    def __init__(self) -> None:
        self.calls: list[dict] = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return DemoPayload(value="ok")


class BrokenInstructorClient:
    def create(self, **kwargs):
        raise RuntimeError("boom")


def test_structured_output_gateway_uses_shared_client_config(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    client = FakeInstructorClient()
    gateway = StructuredOutputGatewayService(
        instructor_client_factory=lambda: client,
        provider_name="litellm",
        model_name="openai/gpt-4o-mini",
        max_retries=2,
        temperature=0.2,
        timeout_seconds=7.5,
    )

    result = gateway.generate(
        caller_name="demo",
        response_model=DemoPayload,
        messages=[{"role": "user", "content": "hi"}],
    )

    assert result == DemoPayload(value="ok")
    assert client.calls[0]["response_model"] is DemoPayload
    assert client.calls[0]["model"] == "openai/gpt-4o-mini"
    assert client.calls[0]["max_retries"] == 2
    assert client.calls[0]["temperature"] == 0.2
    assert client.calls[0]["timeout"] == 7.5


def test_structured_output_gateway_returns_none_when_client_fails(monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    gateway = StructuredOutputGatewayService(
        instructor_client_factory=BrokenInstructorClient,
        provider_name="litellm",
        model_name="openai/gpt-4o-mini",
    )

    result = gateway.generate(
        caller_name="demo",
        response_model=DemoPayload,
        messages=[{"role": "user", "content": "hi"}],
    )

    assert result is None


def test_structured_output_gateway_returns_none_when_provider_is_unsupported() -> None:
    gateway = StructuredOutputGatewayService(
        instructor_client_factory=FakeInstructorClient,
        provider_name="disabled",
        model_name="openai/gpt-4o-mini",
    )

    result = gateway.generate(
        caller_name="demo",
        response_model=DemoPayload,
        messages=[{"role": "user", "content": "hi"}],
    )

    assert result is None


def test_structured_output_gateway_returns_none_when_openai_credentials_are_missing(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    gateway = StructuredOutputGatewayService(
        provider_name="litellm",
        model_name="openai/gpt-4o-mini",
    )

    result = gateway.generate(
        caller_name="demo",
        response_model=DemoPayload,
        messages=[{"role": "user", "content": "hi"}],
    )

    assert result is None
