from __future__ import annotations

import logging
import sys
import time
from pathlib import Path

from sqlalchemy import inspect
from sqlalchemy.exc import OperationalError

from app.core.config import settings
from app.db.base import Base
from app.db.models import GenerationJobEventModel, GenerationJobModel, GenerationResultModel, TrendTemplateModel  # noqa: F401
from app.db.session import get_engine
from app.services.trend_strategy.repository import TrendTemplateRepository

logger = logging.getLogger(__name__)
PROJECT_ROOT = Path(__file__).resolve().parents[3]
ALEMBIC_INI_PATH = PROJECT_ROOT / "alembic.ini"
ALEMBIC_SCRIPT_LOCATION = PROJECT_ROOT / "backend" / "migrations"
UPSTREAM_ALEMBIC_PATH = PROJECT_ROOT.parent / "upstream-materials" / "alembic"
MANAGED_TABLES = {
    "platform_trend_templates",
    "generation_jobs",
    "generation_job_events",
    "generation_results",
}
GENERATION_JOB_REQUIRED_COLUMNS = {
    "current_status": "ALTER TABLE generation_jobs ADD COLUMN current_status VARCHAR(32)",
    "current_stage": "ALTER TABLE generation_jobs ADD COLUMN current_stage VARCHAR(32)",
    "stage_message": "ALTER TABLE generation_jobs ADD COLUMN stage_message TEXT",
    "completed_at": "ALTER TABLE generation_jobs ADD COLUMN completed_at TIMESTAMP",
    "updated_at": "ALTER TABLE generation_jobs ADD COLUMN updated_at TIMESTAMP",
}

try:
    from alembic import command
    from alembic.config import Config
    from alembic.script import ScriptDirectory
except Exception:  # pragma: no cover - depends on optional runtime availability
    if str(UPSTREAM_ALEMBIC_PATH) not in sys.path and UPSTREAM_ALEMBIC_PATH.exists():
        sys.path.insert(0, str(UPSTREAM_ALEMBIC_PATH))
        try:
            from alembic import command
            from alembic.config import Config
            from alembic.script import ScriptDirectory
        except Exception:  # pragma: no cover - depends on optional runtime availability
            command = None
            Config = None
            ScriptDirectory = None
    else:
        command = None
        Config = None
        ScriptDirectory = None


def build_alembic_config():
    if Config is None:
        raise RuntimeError("Alembic is not installed")
    config = Config(str(ALEMBIC_INI_PATH))
    config.set_main_option("script_location", str(ALEMBIC_SCRIPT_LOCATION))
    config.set_main_option("sqlalchemy.url", settings.database_url)
    return config


def run_schema_migrations() -> None:
    if command is None or ScriptDirectory is None:
        raise RuntimeError("Alembic is not installed")

    config = build_alembic_config()
    engine = get_engine()
    existing_tables = set(inspect(engine).get_table_names())
    missing_managed_tables = MANAGED_TABLES - existing_tables
    current_head = ScriptDirectory.from_config(config).get_current_head()

    if "alembic_version" not in existing_tables and existing_tables & MANAGED_TABLES:
        Base.metadata.create_all(bind=engine)
        ensure_legacy_generation_job_columns(engine)
        command.stamp(config, current_head)
        return

    if "alembic_version" in existing_tables and missing_managed_tables:
        Base.metadata.create_all(bind=engine)
        ensure_legacy_generation_job_columns(engine)
        command.stamp(config, current_head)
        return

    command.upgrade(config, "head")


def fallback_schema_bootstrap() -> None:
    logger.warning("Alembic is unavailable; falling back to SQLAlchemy create_all bootstrap")
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    ensure_legacy_generation_job_columns(engine)


def ensure_legacy_generation_job_columns(engine) -> None:
    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())
    if "generation_jobs" not in existing_tables:
        return

    existing_columns = {column["name"] for column in inspector.get_columns("generation_jobs")}
    missing_columns = [name for name in GENERATION_JOB_REQUIRED_COLUMNS if name not in existing_columns]
    if not missing_columns:
        return

    with engine.begin() as connection:
        for column_name in missing_columns:
            connection.exec_driver_sql(GENERATION_JOB_REQUIRED_COLUMNS[column_name])

        connection.exec_driver_sql(
            """
            UPDATE generation_jobs
            SET current_status = COALESCE(
                    current_status,
                    CASE
                        WHEN failed THEN 'FAILED'
                        WHEN timed_out THEN 'TIMEOUT'
                        ELSE 'THEME_PARSING'
                    END
                ),
                current_stage = COALESCE(
                    current_stage,
                    CASE
                        WHEN failed THEN 'FAILED'
                        WHEN timed_out THEN 'TIMEOUT'
                        ELSE 'THEME_PARSING'
                    END
                ),
                stage_message = COALESCE(
                    stage_message,
                    CASE
                        WHEN failed THEN '生成失败'
                        WHEN timed_out THEN '生成超时'
                        ELSE '正在解析创作主题'
                    END
                ),
                updated_at = COALESCE(updated_at, created_at)
            """
        )


def ensure_schema_ready() -> None:
    try:
        run_schema_migrations()
    except RuntimeError as exc:
        if "Alembic is not installed" not in str(exc):
            raise
        fallback_schema_bootstrap()


def bootstrap_database(*, attempts: int | None = None, retry_delay_seconds: float | None = None) -> None:
    max_attempts = attempts or settings.database_bootstrap_attempts
    delay_seconds = retry_delay_seconds if retry_delay_seconds is not None else settings.database_bootstrap_retry_delay_seconds

    last_error: OperationalError | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            ensure_schema_ready()
            TrendTemplateRepository().ensure_seeded()
            return
        except OperationalError as exc:
            last_error = exc
            logger.warning(
                "Database bootstrap attempt %s/%s failed: %s",
                attempt,
                max_attempts,
                exc,
            )
            if attempt >= max_attempts:
                break
            time.sleep(delay_seconds)

    if last_error is not None:
        raise last_error
