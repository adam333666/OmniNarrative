from __future__ import annotations

import os
from pathlib import Path

import pytest

TEST_DB_PATH = Path("/tmp/multi_media_test.db")
TEST_CHECKPOINT_PATH = Path("/tmp/multi_media_langgraph_checkpoint_test.sqlite")
os.environ.setdefault("DATABASE_URL", f"sqlite+pysqlite:///{TEST_DB_PATH}")

from app.api.routes.internal import get_generation_checkpoints
from app.db.bootstrap import bootstrap_database
from app.db.repositories.generation_job_event_repository import SqlAlchemyGenerationJobEventRepository
from app.db.repositories.generation_job_repository import SqlAlchemyGenerationJobRepository
from app.db.repositories.generation_result_repository import SqlAlchemyGenerationResultRepository
from app.db.session import get_engine, get_session_factory
from app.schemas.creation_request import CreationRequest
from app.schemas.narrative_package import KeyShot, ScriptSegment
from app.schemas.profiles import AudienceProfile, StyleProfile
from app.schemas.trend_template import PlatformTrendTemplate
from app.services.generation_pipeline.checkpointer import generation_checkpoint_service
from app.services.generation_pipeline.orchestrator import generation_execution_orchestrator
from app.services.generation_pipeline.runner import generation_execution_runner
from app.services.generation_pipeline.result_builder import generation_result_builder
from app.services.generation_pipeline.store import generation_pipeline_store
from app.services.narrative_generator.service import NarrativeBundleResult, NarrativeGenerationRuntime


def reset_database() -> None:
    get_engine().dispose()
    generation_checkpoint_service.reset(sqlite_path=TEST_CHECKPOINT_PATH)
    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink()
    if TEST_CHECKPOINT_PATH.exists():
        TEST_CHECKPOINT_PATH.unlink()
    get_engine.cache_clear()
    get_session_factory.cache_clear()
    generation_execution_runner.shutdown(wait=False)
    bootstrap_database()
    generation_pipeline_store.repository = SqlAlchemyGenerationJobRepository()
    generation_pipeline_store.result_repository = SqlAlchemyGenerationResultRepository()
    generation_pipeline_store.event_repository = SqlAlchemyGenerationJobEventRepository()
    generation_result_builder.result_repository = SqlAlchemyGenerationResultRepository()
    generation_execution_orchestrator.graph = None


def build_request() -> CreationRequest:
    return CreationRequest(
        theme_text="时间旅行悖论",
        content_type="science_popularization",
        target_platform="bilibili",
        target_audience_text="18到28岁，喜欢科幻设定和逻辑推理的观众",
        style_tone="suspense",
        custom_style_text="保持一点烧脑感",
    )


def test_langgraph_checkpoint_is_persisted_and_queryable(monkeypatch) -> None:
    reset_database()
    created = generation_pipeline_store.create(build_request())
    generation_pipeline_store.mark_ready_for_result(created.generation_id)
    record = generation_pipeline_store.get_record(created.generation_id)

    monkeypatch.setattr(
        "app.services.generation_pipeline.orchestrator.profile_parser_service.parse_audience_profile",
        lambda request: AudienceProfile(
            raw_text=request.target_audience_text,
            age_group_guess="18-24",
            interest_tags=["脑洞设定"],
            pain_points=["复杂概念理解门槛高"],
            content_preference=["开头要快"],
            emotion_preference=["希望被带入但不被说教"],
        ),
    )
    monkeypatch.setattr(
        "app.services.generation_pipeline.orchestrator.profile_parser_service.parse_style_profile",
        lambda request: StyleProfile(
            style_label=request.style_tone,
            emotion_label="紧张好奇",
            intensity_level="medium",
            custom_notes=request.custom_style_text,
        ),
    )
    monkeypatch.setattr(
        "app.services.generation_pipeline.orchestrator.trend_strategy_service.get_template",
        lambda request, audience_profile: PlatformTrendTemplate(
            platform=request.target_platform,
            content_type=request.content_type,
            summary="平台节奏偏强钩子",
            hook_patterns=["先抛问题"],
            rhythm_patterns=["快切进入"],
            title_cover_style=["高信息密度", "强对比标题"],
            audience_preference_summary="偏好高信息密度和快速进入主题的表达。",
            avoid_patterns=["铺垫过长"],
            hot_topics_summary=["时间悖论", "科幻设定拆解"],
            source_type="db_truth",
            updated_at="2026-03-27T00:00:00+00:00",
        ),
    )
    monkeypatch.setattr(
        "app.services.generation_pipeline.orchestrator.narrative_generator_service.build_narrative_bundle_result",
        lambda *args, **kwargs: NarrativeBundleResult(
            title="时间旅行悖论，为什么会让人越想越上头？",
            one_sentence_summary="一条能兼顾理解与传播的方案。",
            segments=[
                ScriptSegment(
                    segment_number=1,
                    segment_title="开头",
                    segment_goal="抓住注意力",
                    narration="n",
                    subtitle_text="s",
                    visual_description="v",
                    emotion="紧张好奇",
                    rhythm="快切进入",
                )
            ],
            key_shots=[
                KeyShot(
                    shot_title="钩子镜头",
                    shot_focus="第一句问题",
                    shot_duration_seconds=4,
                    transition_hint="直接切入",
                )
            ],
            title_alternatives=["标题备选"],
            hook_alternatives=["钩子备选"],
            runtime=NarrativeGenerationRuntime(
                source_type="structured_output_gateway",
                fallback_reason=None,
            ),
        ),
    )

    result = generation_execution_orchestrator.execute(record)
    checkpoints = generation_checkpoint_service.list_checkpoints(created.generation_id)
    response = get_generation_checkpoints(created.generation_id, limit=20)

    assert result.export_meta["generation_id"] == created.generation_id
    assert TEST_CHECKPOINT_PATH.exists()
    assert len(checkpoints) >= 1
    assert response.generation_id == created.generation_id
    assert response.total >= 1
    assert "record" in response.items[0].channel_keys


def test_checkpoint_query_requires_existing_generation() -> None:
    reset_database()

    with pytest.raises(Exception) as exc_info:
        get_generation_checkpoints("missing-generation", limit=20)

    assert "Generation not found" in str(exc_info.value)
