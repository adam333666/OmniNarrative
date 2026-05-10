"""initialize truth tables

Revision ID: 20260325_091900
Revises:
Create Date: 2026-03-25 09:19:00
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260325_091900"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "generation_jobs",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("generation_id", sa.String(length=32), nullable=False),
        sa.Column("request_payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("failed", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("timed_out", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("failure_reason", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("generation_id", name="uq_generation_jobs_generation_id"),
    )
    op.create_index(op.f("ix_generation_jobs_created_at"), "generation_jobs", ["created_at"], unique=False)
    op.create_index(op.f("ix_generation_jobs_generation_id"), "generation_jobs", ["generation_id"], unique=False)

    op.create_table(
        "generation_results",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("generation_id", sa.String(length=32), nullable=False),
        sa.Column("result_payload", sa.JSON(), nullable=False),
        sa.Column("generated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("generation_id", name="uq_generation_results_generation_id"),
    )
    op.create_index(op.f("ix_generation_results_generated_at"), "generation_results", ["generated_at"], unique=False)
    op.create_index(op.f("ix_generation_results_generation_id"), "generation_results", ["generation_id"], unique=False)

    op.create_table(
        "platform_trend_templates",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("platform", sa.String(length=64), nullable=False),
        sa.Column("content_type", sa.String(length=64), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("hook_patterns", sa.JSON(), nullable=False),
        sa.Column("rhythm_patterns", sa.JSON(), nullable=False),
        sa.Column("title_cover_style", sa.JSON(), nullable=False),
        sa.Column("audience_preference_summary", sa.Text(), nullable=False),
        sa.Column("avoid_patterns", sa.JSON(), nullable=False),
        sa.Column("hot_topics_summary", sa.JSON(), nullable=False),
        sa.Column("source_type", sa.String(length=32), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("platform", "content_type", name="uq_platform_content_type"),
    )
    op.create_index(op.f("ix_platform_trend_templates_content_type"), "platform_trend_templates", ["content_type"], unique=False)
    op.create_index(op.f("ix_platform_trend_templates_platform"), "platform_trend_templates", ["platform"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_platform_trend_templates_platform"), table_name="platform_trend_templates")
    op.drop_index(op.f("ix_platform_trend_templates_content_type"), table_name="platform_trend_templates")
    op.drop_table("platform_trend_templates")

    op.drop_index(op.f("ix_generation_results_generation_id"), table_name="generation_results")
    op.drop_index(op.f("ix_generation_results_generated_at"), table_name="generation_results")
    op.drop_table("generation_results")

    op.drop_index(op.f("ix_generation_jobs_generation_id"), table_name="generation_jobs")
    op.drop_index(op.f("ix_generation_jobs_created_at"), table_name="generation_jobs")
    op.drop_table("generation_jobs")
