from fastapi import Header, HTTPException

from app.core.config import settings


def get_settings():
    return settings


def require_internal_api_key(
    x_internal_api_key: str = Header(default="", alias="X-Internal-Api-Key"),
) -> None:
    if not settings.internal_api_key:
        raise HTTPException(status_code=503, detail="Internal API is not enabled in the current environment")

    if x_internal_api_key != settings.internal_api_key:
        raise HTTPException(status_code=403, detail="Invalid internal API key")
