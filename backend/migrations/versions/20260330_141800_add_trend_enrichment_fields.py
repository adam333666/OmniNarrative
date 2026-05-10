"""add trend enrichment fields

Revision ID: 20260330_141800
Revises: 20260327_182500
Create Date: 2026-03-30 14:18:00
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "20260330_141800"
down_revision: str | None = "20260327_182500"
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "platform_trend_templates",
        sa.Column("interaction_patterns", sa.JSON(), nullable=False, server_default=sa.text("'[]'")),
    )
    op.add_column(
        "platform_trend_templates",
        sa.Column("emotional_entry_points", sa.JSON(), nullable=False, server_default=sa.text("'[]'")),
    )
    op.add_column(
        "platform_trend_templates",
        sa.Column("creator_angle_summary", sa.Text(), nullable=False, server_default=""),
    )


def downgrade() -> None:
    op.drop_column("platform_trend_templates", "creator_angle_summary")
    op.drop_column("platform_trend_templates", "emotional_entry_points")
    op.drop_column("platform_trend_templates", "interaction_patterns")
