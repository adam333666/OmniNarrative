from __future__ import annotations

from app.services.trend_strategy.service import trend_strategy_service


def main() -> None:
    response = trend_strategy_service.refresh_templates()
    print(f"Refreshed {response.refreshed_count} templates at {response.updated_at.isoformat()}")
    for item in response.items:
        print(f"- {item.platform}/{item.content_type}: {item.summary}")


if __name__ == "__main__":
    main()
