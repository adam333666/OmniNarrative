"""add generation job status columns

Revision ID: 20260327_103900
Revises: 20260325_091900
Create Date: 2026-03-27 10:39:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260327_103900"
down_revision = "20260325_091900"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "generation_jobs",
        sa.Column("current_status", sa.String(length=32), nullable=False, server_default="THEME_PARSING"),
    )
    op.add_column(
        "generation_jobs",
        sa.Column("current_stage", sa.String(length=32), nullable=False, server_default="THEME_PARSING"),
    )
    op.add_column(
        "generation_jobs",
        sa.Column("stage_message", sa.Text(), nullable=False, server_default="正在解析创作主题"),
    )
    op.add_column(
        "generation_jobs",
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "generation_jobs",
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index(op.f("ix_generation_jobs_updated_at"), "generation_jobs", ["updated_at"], unique=False)

    op.execute(
        """
        UPDATE generation_jobs
        SET current_status = CASE
                WHEN failed THEN 'FAILED'
                WHEN timed_out THEN 'TIMEOUT'
                ELSE 'THEME_PARSING'
            END,
            current_stage = CASE
                WHEN failed THEN 'FAILED'
                WHEN timed_out THEN 'TIMEOUT'
                ELSE 'THEME_PARSING'
            END,
            stage_message = CASE
                WHEN failed THEN '生成失败'
                WHEN timed_out THEN '生成超时'
                ELSE '正在解析创作主题'
            END,
            updated_at = COALESCE(updated_at, created_at)
        """
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_generation_jobs_updated_at"), table_name="generation_jobs")
    op.drop_column("generation_jobs", "updated_at")
    op.drop_column("generation_jobs", "completed_at")
    op.drop_column("generation_jobs", "stage_message")
    op.drop_column("generation_jobs", "current_stage")
    op.drop_column("generation_jobs", "current_status")
