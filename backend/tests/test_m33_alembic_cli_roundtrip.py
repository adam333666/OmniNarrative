from __future__ import annotations

import os
import sqlite3
import subprocess
from pathlib import Path

from alembic.config import Config
from alembic.script import ScriptDirectory


PROJECT_ROOT = Path("/home/admin2/smy/multi-media")
ALEMBIC_INI = PROJECT_ROOT / "alembic.ini"
ALEMBIC_CONFIG = Config(str(ALEMBIC_INI))
ALEMBIC_CONFIG.set_main_option("script_location", str(PROJECT_ROOT / "backend" / "migrations"))
EXPECTED_HEAD_REVISION = ScriptDirectory.from_config(ALEMBIC_CONFIG).get_current_head()


def run_alembic(db_path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["DATABASE_URL"] = f"sqlite+pysqlite:///{db_path}"
    return subprocess.run(
        ["python3", "-m", "alembic", "-c", str(ALEMBIC_INI), *args],
        cwd=PROJECT_ROOT,
        env=env,
        check=True,
        capture_output=True,
        text=True,
    )


def list_tables(db_path: Path) -> set[str]:
    connection = sqlite3.connect(db_path)
    try:
        return {
            row[0]
            for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")
        }
    finally:
        connection.close()


def test_alembic_cli_can_upgrade_downgrade_and_upgrade_again(tmp_path) -> None:
    db_path = tmp_path / "alembic_roundtrip.db"

    run_alembic(db_path, "upgrade", "head")
    upgraded_tables = list_tables(db_path)
    assert "alembic_version" in upgraded_tables
    assert "generation_jobs" in upgraded_tables
    assert "generation_job_events" in upgraded_tables
    assert "generation_results" in upgraded_tables
    assert "platform_trend_templates" in upgraded_tables

    run_alembic(db_path, "downgrade", "base")
    downgraded_tables = list_tables(db_path)
    assert "generation_jobs" not in downgraded_tables
    assert "generation_job_events" not in downgraded_tables
    assert "generation_results" not in downgraded_tables
    assert "platform_trend_templates" not in downgraded_tables

    run_alembic(db_path, "upgrade", "head")
    roundtrip_tables = list_tables(db_path)
    assert "generation_jobs" in roundtrip_tables
    assert "generation_job_events" in roundtrip_tables
    assert "generation_results" in roundtrip_tables
    assert "platform_trend_templates" in roundtrip_tables

    current = run_alembic(db_path, "current")
    assert EXPECTED_HEAD_REVISION in current.stdout or EXPECTED_HEAD_REVISION in current.stderr
