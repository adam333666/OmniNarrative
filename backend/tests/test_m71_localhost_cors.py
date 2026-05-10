from __future__ import annotations

import asyncio

from app.main import app


async def send_options_request(origin: str) -> tuple[int, dict[str, str]]:
    headers = [
        (b"host", b"testserver"),
        (b"origin", origin.encode("utf-8")),
        (b"access-control-request-method", b"GET"),
    ]
    scope = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": "OPTIONS",
        "scheme": "http",
        "path": "/api/v1/config/input-options",
        "raw_path": b"/api/v1/config/input-options",
        "query_string": b"",
        "headers": headers,
        "client": ("127.0.0.1", 12345),
        "server": ("testserver", 80),
    }
    messages: list[dict] = []

    async def receive() -> dict:
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message: dict) -> None:
        messages.append(message)

    await app(scope, receive, send)

    start_message = next(message for message in messages if message["type"] == "http.response.start")
    response_headers = {
        key.decode("utf-8"): value.decode("utf-8")
        for key, value in start_message["headers"]
    }
    return start_message["status"], response_headers


def test_cors_allows_localhost_origins_on_non_default_ports() -> None:
    status_code, headers = asyncio.run(send_options_request("http://127.0.0.1:3100"))

    assert status_code == 200
    assert headers["access-control-allow-origin"] == "http://127.0.0.1:3100"


def test_cors_rejects_unknown_origins() -> None:
    status_code, _headers = asyncio.run(send_options_request("https://evil.example.com"))

    assert status_code == 400
