from __future__ import annotations

import os
from pathlib import Path

TEST_DB_PATH = Path("/tmp/multi_media_test.db")
TEST_CHECKPOINT_PATH = Path("/tmp/multi_media_langgraph_checkpoint_test.sqlite")
os.environ.setdefault("DATABASE_URL", f"sqlite+pysqlite:///{TEST_DB_PATH}")

from app.db.bootstrap import bootstrap_database
from app.db.repositories.generation_job_event_repository import SqlAlchemyGenerationJobEventRepository
from app.db.repositories.generation_job_repository import SqlAlchemyGenerationJobRepository
from app.db.repositories.generation_result_repository import SqlAlchemyGenerationResultRepository
from app.db.session import get_engine, get_session_factory
from app.schemas.creation_request import CreationRequest
from app.schemas.narrative_package import KeyShot, ScriptSegment, StructuredTextCandidate
from app.schemas.profiles import AudienceProfile, StyleProfile
from app.schemas.trend_template import PlatformTrendTemplate
from app.services.generation_pipeline.checkpointer import generation_checkpoint_service
from app.services.generation_pipeline.orchestrator import generation_execution_orchestrator
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
    bootstrap_database()
    generation_pipeline_store.repository = SqlAlchemyGenerationJobRepository()
    generation_pipeline_store.result_repository = SqlAlchemyGenerationResultRepository()
    generation_pipeline_store.event_repository = SqlAlchemyGenerationJobEventRepository()
    generation_result_builder.result_repository = SqlAlchemyGenerationResultRepository()
    generation_execution_orchestrator.graph = None


def build_request() -> CreationRequest:
    return CreationRequest(
        theme_text="为什么别人总记不住你的表达重点",
        content_type="knowledge_share",
        target_platform="bilibili",
        target_audience_text="希望提升表达效率和观点组织能力的年轻人",
        style_tone="clear",
        custom_style_text="更像拆解问题，不要太鸡汤",
    )


def patch_generation_dependencies(monkeypatch) -> None:
    monkeypatch.setattr(
        "app.services.generation_pipeline.orchestrator.profile_parser_service.parse_audience_profile",
        lambda request: AudienceProfile(
            raw_text=request.target_audience_text,
            age_group_guess="22-28",
            interest_tags=["表达效率"],
            pain_points=["说了很多但重点不突出"],
            content_preference=["问题拆解"],
            emotion_preference=["希望直接获得方法"],
        ),
    )
    monkeypatch.setattr(
        "app.services.generation_pipeline.orchestrator.profile_parser_service.parse_style_profile",
        lambda request: StyleProfile(
            style_label=request.style_tone,
            emotion_label="直接清楚",
            intensity_level="medium",
            custom_notes=request.custom_style_text,
        ),
    )
    monkeypatch.setattr(
        "app.services.generation_pipeline.orchestrator.trend_strategy_service.get_template",
        lambda request, audience_profile: PlatformTrendTemplate(
            platform=request.target_platform,
            content_type=request.content_type,
            summary="适合问题拆解和强结构表达。",
            hook_patterns=["先抛一个常见误解"],
            rhythm_patterns=["问题-原因-方法"],
            title_cover_style=["强结论标题", "对比式封面"],
            audience_preference_summary="偏好快速进入问题并给出结构化答案。",
            avoid_patterns=["空泛感悟"],
            hot_topics_summary=["表达重点", "沟通结构"],
            source_type="db_truth",
            updated_at="2026-03-27T00:00:00+00:00",
        ),
    )
    monkeypatch.setattr(
        "app.services.generation_pipeline.orchestrator.narrative_generator_service.build_narrative_bundle_result",
        lambda *args, **kwargs: NarrativeBundleResult(
            title="为什么你说了很多，别人还是没记住重点？",
            one_sentence_summary="把表达无效的根因拆成一条更好吸收的脚本。",
            segments=[
                ScriptSegment(
                    segment_number=1,
                    segment_title="问题切入",
                    segment_goal="建立共鸣",
                    narration="n1",
                    subtitle_text="s1",
                    visual_description="v1",
                    emotion="直接清楚",
                    rhythm="问题-原因-方法",
                )
            ],
            key_shots=[
                KeyShot(
                    shot_title="会议瞬间",
                    shot_focus="别人听完点头但没记住",
                    shot_duration_seconds=4,
                    transition_hint="直接切入",
                )
            ],
            title_alternatives=["你不是不会说，是重点没有被托起来"],
            hook_alternatives=["很多表达无效，不是内容少，而是结构太散"],
            title_candidates=[
                StructuredTextCandidate(
                    candidate_text="你不是不会说，是重点没有被托起来",
                    usage_scenario="结果页标题候选",
                    design_reason="用于保持 result builder 测试夹具与真实 schema 一致。",
                )
            ],
            hook_candidates=[
                StructuredTextCandidate(
                    candidate_text="很多表达无效，不是内容少，而是结构太散",
                    usage_scenario="结果页钩子候选",
                    design_reason="用于保持 result builder 测试夹具与真实 schema 一致。",
                )
            ],
            runtime=NarrativeGenerationRuntime(
                source_type="structured_output_gateway",
                fallback_reason=None,
            ),
        ),
    )


def test_result_builder_restores_from_checkpoint_before_rerun(monkeypatch) -> None:
    reset_database()
    created = generation_pipeline_store.create(build_request())
    generation_pipeline_store.mark_ready_for_result(created.generation_id)
    record = generation_pipeline_store.get_record(created.generation_id)
    patch_generation_dependencies(monkeypatch)

    initial_result = generation_execution_orchestrator.execute(record)
    assert generation_pipeline_store.result_repository.get(created.generation_id) is None

    monkeypatch.setattr(
        "app.services.generation_pipeline.coordinator.generation_execution_orchestrator.execute",
        lambda record: (_ for _ in ()).throw(AssertionError("should not rerun orchestrator when checkpoint snapshot exists")),
    )

    restored_result = generation_result_builder.build(created.generation_id)
    saved_result = generation_pipeline_store.result_repository.get(created.generation_id)
    status = generation_pipeline_store.get_status(created.generation_id)

    assert restored_result.export_meta["generation_id"] == created.generation_id
    assert restored_result.export_meta == initial_result.export_meta
    assert saved_result is not None
    assert saved_result.export_meta["generation_id"] == created.generation_id
    assert str(status.status) == "DONE"
