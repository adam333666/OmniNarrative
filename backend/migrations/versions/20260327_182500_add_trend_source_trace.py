"""add trend source trace

Revision ID: 20260327_182500
Revises: 20260327_111000
Create Date: 2026-03-27 18:25:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260327_182500"
down_revision = "20260327_111000"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "platform_trend_templates",
        sa.Column("source_trace", sa.JSON(), nullable=False, server_default=sa.text("'[]'")),
    )


def downgrade() -> None:
    op.drop_column("platform_trend_templates", "source_trace")
