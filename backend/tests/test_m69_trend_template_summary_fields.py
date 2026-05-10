from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("DATABASE_URL", f"sqlite+pysqlite:///{Path('/tmp/multi_media_test_stage.db')}")

from app.db.base import Base
from app.db.session import get_engine
from app.services.trend_strategy.default_templates import build_refreshed_templates
from app.services.trend_strategy.service import trend_strategy_service


def test_trend_template_summary_includes_structured_strategy_fields() -> None:
    Base.metadata.create_all(bind=get_engine())
    trend_strategy_service.repository.save_templates(build_refreshed_templates())
    response = trend_strategy_service.list_template_summaries(platform="bilibili", content_type=None)

    assert response.total >= 1
    item = response.items[0]
    assert len(item.hook_patterns) >= 2
    assert len(item.rhythm_patterns) >= 2
    assert len(item.title_cover_style) >= 2
    assert item.audience_preference_summary
    assert len(item.avoid_patterns) >= 2
    assert len(item.hot_topics_summary) >= 2
    assert len(item.interaction_patterns) >= 2
    assert len(item.emotional_entry_points) >= 2
    assert item.creator_angle_summary
    assert isinstance(item.source_trace, list)
    assert len(item.configured_sources) >= 1
