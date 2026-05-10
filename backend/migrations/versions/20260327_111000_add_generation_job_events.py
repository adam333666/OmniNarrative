"""add generation job events

Revision ID: 20260327_111000
Revises: 20260327_103900
Create Date: 2026-03-27 11:10:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260327_111000"
down_revision = "20260327_103900"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "generation_job_events",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("generation_id", sa.String(length=32), nullable=False),
        sa.Column("event_type", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("stage", sa.String(length=32), nullable=False),
        sa.Column("stage_message", sa.Text(), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_generation_job_events_generation_id"), "generation_job_events", ["generation_id"], unique=False)
    op.create_index(op.f("ix_generation_job_events_event_type"), "generation_job_events", ["event_type"], unique=False)
    op.create_index(op.f("ix_generation_job_events_occurred_at"), "generation_job_events", ["occurred_at"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_generation_job_events_occurred_at"), table_name="generation_job_events")
    op.drop_index(op.f("ix_generation_job_events_event_type"), table_name="generation_job_events")
    op.drop_index(op.f("ix_generation_job_events_generation_id"), table_name="generation_job_events")
    op.drop_table("generation_job_events")
