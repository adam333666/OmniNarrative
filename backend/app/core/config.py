from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "multi-media-backend"
    app_env: str = "development"
    api_prefix: str = "/api/v1"
    database_url: str = "postgresql+psycopg://postgres:postgres@db:5432/multi_media"
    database_bootstrap_attempts: int = 5
    database_bootstrap_retry_delay_seconds: float = 1.0
    internal_api_key: str | None = None
    trend_templates_seed_path: Path = Path(__file__).resolve().parents[1] / "data" / "platform_trend_templates.json"
    model_provider: str = "litellm"
    model_name: str = "openai/gpt-4o-mini"
    model_timeout_seconds: float = 20.0
    model_max_retries: int = 1
    model_temperature: float = 0.4
    generation_auto_start_enabled: bool = True
    generation_background_workers: int = 2
    generation_checkpoint_sqlite_path: Path = Path("/tmp/multi_media_langgraph_checkpoints.sqlite")
    trend_rsshub_base_url: str | None = None
    trend_rsshub_platform_routes: dict[str, list[str] | str] = {}
    trend_rsshub_item_limit: int = 5
    aihubmix_api_key: str | None = None
    aihubmix_base_url: str | None = None
    aihubmix_search_model: str = "gemini-3.1-flash-lite-preview"
    aihubmix_timeout_seconds: float = 45.0

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
