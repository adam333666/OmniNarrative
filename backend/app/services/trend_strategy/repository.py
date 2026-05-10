from __future__ import annotations

import json
from pathlib import Path

from app.core.config import settings
from app.db.repositories.trend_template_repository import SqlAlchemyTrendTemplateRepository
from app.schemas.trend_template import PlatformTrendTemplate
from app.services.trend_strategy.default_templates import build_seed_templates


class TrendTemplateRepository:
    def __init__(
        self,
        seed_path: Path | None = None,
        database_repository: SqlAlchemyTrendTemplateRepository | None = None,
    ) -> None:
        self.seed_path = seed_path or settings.trend_templates_seed_path
        self.database_repository = database_repository or SqlAlchemyTrendTemplateRepository()

    def ensure_seeded(self) -> None:
        if self.database_repository.count() > 0:
            return
        self.save_templates(self._load_seed_templates())

    def _load_seed_templates(self) -> list[PlatformTrendTemplate]:
        self.seed_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.seed_path.exists():
            templates = build_seed_templates()
            payload = [item.model_dump(mode="json") for item in templates]
            self.seed_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            return templates

        raw_items = json.loads(self.seed_path.read_text(encoding="utf-8"))
        return [PlatformTrendTemplate.model_validate(item) for item in raw_items]

    def list_templates(self, platform: str | None = None, content_type: str | None = None) -> list[PlatformTrendTemplate]:
        self.ensure_seeded()
        return self.database_repository.list_templates(platform=platform, content_type=content_type)

    def save_templates(self, templates: list[PlatformTrendTemplate]) -> None:
        self.database_repository.save_templates(templates)

    def write_seed_templates(self, templates: list[PlatformTrendTemplate]) -> None:
        self.seed_path.parent.mkdir(parents=True, exist_ok=True)
        ordered_templates = sorted(templates, key=lambda item: (item.platform, item.content_type))
        payload = [item.model_dump(mode="json") for item in ordered_templates]
        self.seed_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def get_best_match(self, platform: str, content_type: str) -> PlatformTrendTemplate | None:
        self.ensure_seeded()
        return self.database_repository.get_best_match(platform=platform, content_type=content_type)
