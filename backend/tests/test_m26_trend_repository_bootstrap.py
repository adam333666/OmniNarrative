from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("DATABASE_URL", f"sqlite+pysqlite:///{Path('/tmp/multi_media_test.db')}")

from app.db.base import Base
from app.db.bootstrap import bootstrap_database
from app.db.session import get_engine
from app.services.trend_strategy.repository import TrendTemplateRepository


def test_trend_repository_bootstrap_seeds_database() -> None:
    engine = get_engine()
    Base.metadata.drop_all(bind=engine)

    bootstrap_database()

    repository = TrendTemplateRepository()
    templates = repository.list_templates()

    assert len(templates) >= 5
    assert any(item.platform == "bilibili" for item in templates)


def test_trend_repository_can_overwrite_existing_template() -> None:
    bootstrap_database()
    repository = TrendTemplateRepository()
    template = repository.get_best_match(platform="bilibili", content_type="science_popularization")
    assert template is not None

    updated = template.model_copy(update={"summary": "数据库仓已接管趋势模板真值。", "source_type": "database_seed"})
    repository.save_templates([updated])

    refreshed = repository.get_best_match(platform="bilibili", content_type="science_popularization")
    assert refreshed is not None
    assert refreshed.summary == "数据库仓已接管趋势模板真值。"
    assert refreshed.source_type == "database_seed"
