from __future__ import annotations

import os
import sqlite3
from pathlib import Path

os.environ.setdefault("DATABASE_URL", f"sqlite+pysqlite:///{Path('/tmp/multi_media_test.db')}")

from sqlalchemy.exc import OperationalError

from app.core.config import settings
from app.db.bootstrap import bootstrap_database
from app.db.session import get_engine, get_session_factory


def test_bootstrap_database_retries_until_schema_bootstrap_succeeds(monkeypatch) -> None:
    attempts = {"count": 0}

    def fake_ensure_schema_ready() -> None:
        attempts["count"] += 1
        if attempts["count"] < 3:
            raise OperationalError("create table", {}, RuntimeError("db not ready"))

    monkeypatch.setattr("app.db.bootstrap.ensure_schema_ready", fake_ensure_schema_ready)
    monkeypatch.setattr("app.db.bootstrap.TrendTemplateRepository.ensure_seeded", lambda self: None)
    monkeypatch.setattr("app.db.bootstrap.time.sleep", lambda _seconds: None)

    bootstrap_database(attempts=3, retry_delay_seconds=0)

    assert attempts["count"] == 3


def test_bootstrap_database_raises_after_retry_budget_is_exhausted(monkeypatch) -> None:
    monkeypatch.setattr(
        "app.db.bootstrap.ensure_schema_ready",
        lambda: (_ for _ in ()).throw(OperationalError("create table", {}, RuntimeError("db not ready"))),
    )
    monkeypatch.setattr("app.db.bootstrap.time.sleep", lambda _seconds: None)

    try:
        bootstrap_database(attempts=2, retry_delay_seconds=0)
    except OperationalError:
        pass
    else:
        raise AssertionError("Expected bootstrap_database to raise after exhausting retries")


def test_bootstrap_database_adds_missing_result_table_without_dropping_existing_jobs(tmp_path, monkeypatch) -> None:
    db_path = tmp_path / "legacy_bootstrap.db"
    monkeypatch.setattr(settings, "database_url", f"sqlite+pysqlite:///{db_path}")
    get_engine.cache_clear()
    get_session_factory.cache_clear()

    connection = sqlite3.connect(db_path)
    connection.execute(
        """
        CREATE TABLE generation_jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            generation_id VARCHAR(32) NOT NULL,
            request_payload JSON NOT NULL,
            created_at DATETIME NOT NULL,
            failed BOOLEAN NOT NULL DEFAULT 0,
            timed_out BOOLEAN NOT NULL DEFAULT 0,
            failure_reason TEXT
        )
        """
    )
    connection.execute(
        "CREATE UNIQUE INDEX uq_generation_jobs_generation_id ON generation_jobs (generation_id)"
    )
    connection.execute(
        """
        INSERT INTO generation_jobs (
            generation_id, request_payload, created_at, failed, timed_out, failure_reason
        ) VALUES (
            'gen_legacy001',
            '{"theme_text":"legacy"}',
            '2026-03-25 09:00:00',
            0,
            0,
            NULL
        )
        """
    )
    connection.commit()
    connection.close()

    bootstrap_database(attempts=1, retry_delay_seconds=0)

    connection = sqlite3.connect(db_path)
    tables = {
        row[0]
        for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")
    }
    job_count = connection.execute("SELECT COUNT(*) FROM generation_jobs").fetchone()[0]
    connection.close()

    assert "generation_jobs" in tables
    assert "generation_job_events" in tables
    assert "generation_results" in tables
    assert "platform_trend_templates" in tables
    assert job_count == 1


def test_bootstrap_database_backfills_generation_job_status_columns_for_legacy_schema(tmp_path, monkeypatch) -> None:
    db_path = tmp_path / "legacy_generation_status.db"
    monkeypatch.setattr(settings, "database_url", f"sqlite+pysqlite:///{db_path}")
    get_engine.cache_clear()
    get_session_factory.cache_clear()

    connection = sqlite3.connect(db_path)
    connection.execute(
        """
        CREATE TABLE generation_jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            generation_id VARCHAR(32) NOT NULL,
            request_payload JSON NOT NULL,
            created_at DATETIME NOT NULL,
            failed BOOLEAN NOT NULL DEFAULT 0,
            timed_out BOOLEAN NOT NULL DEFAULT 0,
            failure_reason TEXT
        )
        """
    )
    connection.execute("CREATE UNIQUE INDEX uq_generation_jobs_generation_id ON generation_jobs (generation_id)")
    connection.execute(
        """
        INSERT INTO generation_jobs (
            generation_id, request_payload, created_at, failed, timed_out, failure_reason
        ) VALUES (
            'gen_legacy002',
            '{"theme_text":"legacy"}',
            '2026-03-25 09:00:00',
            0,
            0,
            NULL
        )
        """
    )
    connection.commit()
    connection.close()

    bootstrap_database(attempts=1, retry_delay_seconds=0)

    connection = sqlite3.connect(db_path)
    columns = {
        row[1]
        for row in connection.execute("PRAGMA table_info(generation_jobs)")
    }
    row = connection.execute(
        """
        SELECT current_status, current_stage, stage_message, updated_at
        FROM generation_jobs
        WHERE generation_id = 'gen_legacy002'
        """
    ).fetchone()
    connection.close()

    assert {"current_status", "current_stage", "stage_message", "updated_at", "completed_at"} <= columns
    assert row == ("THEME_PARSING", "THEME_PARSING", "正在解析创作主题", "2026-03-25 09:00:00")


def test_bootstrap_database_falls_back_to_create_all_when_alembic_is_unavailable(monkeypatch) -> None:
    attempts = {"fallback_called": 0}

    monkeypatch.setattr(
        "app.db.bootstrap.run_schema_migrations",
        lambda: (_ for _ in ()).throw(RuntimeError("Alembic is not installed")),
    )

    def fake_fallback() -> None:
        attempts["fallback_called"] += 1

    monkeypatch.setattr("app.db.bootstrap.fallback_schema_bootstrap", fake_fallback)
    monkeypatch.setattr("app.db.bootstrap.TrendTemplateRepository.ensure_seeded", lambda self: None)

    bootstrap_database(attempts=1, retry_delay_seconds=0)

    assert attempts["fallback_called"] == 1


def test_bootstrap_database_repairs_missing_tables_even_if_alembic_version_exists(tmp_path, monkeypatch) -> None:
    db_path = tmp_path / "stale_version.db"
    monkeypatch.setattr(settings, "database_url", f"sqlite+pysqlite:///{db_path}")
    get_engine.cache_clear()
    get_session_factory.cache_clear()

    connection = sqlite3.connect(db_path)
    connection.execute("CREATE TABLE alembic_version (version_num VARCHAR(32) NOT NULL)")
    connection.execute("INSERT INTO alembic_version (version_num) VALUES ('20260325_091900')")
    connection.commit()
    connection.close()

    bootstrap_database(attempts=1, retry_delay_seconds=0)

    connection = sqlite3.connect(db_path)
    tables = {
        row[0]
        for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")
    }
    connection.close()

    assert "generation_jobs" in tables
    assert "generation_job_events" in tables
    assert "generation_results" in tables
    assert "platform_trend_templates" in tables
