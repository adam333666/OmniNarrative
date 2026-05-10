from __future__ import annotations

import os
from pathlib import Path

TEST_DB_PATH = Path("/tmp/multi_media_test.db")
TEST_CHECKPOINT_PATH = Path("/tmp/multi_media_langgraph_checkpoint_test.sqlite")
os.environ.setdefault("DATABASE_URL", f"sqlite+pysqlite:///{TEST_DB_PATH}")

from app.api.routes.internal import restore_generation_from_latest_checkpoint
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
        theme_text="熬夜后为什么更容易情绪化",
        content_type="knowledge_share",
        target_platform="xiaohongshu",
        target_audience_text="22到30岁的都市上班族，希望快速理解身心状态变化",
        style_tone="calm",
        custom_style_text="解释要清晰，不要太说教",
    )


def patch_generation_dependencies(monkeypatch) -> None:
    monkeypatch.setattr(
        "app.services.generation_pipeline.orchestrator.profile_parser_service.parse_audience_profile",
        lambda request: AudienceProfile(
            raw_text=request.target_audience_text,
            age_group_guess="25-30",
            interest_tags=["情绪管理"],
            pain_points=["作息混乱后状态波动"],
            content_preference=["结论先行"],
            emotion_preference=["平静但有被理解的感觉"],
        ),
    )
    monkeypatch.setattr(
        "app.services.generation_pipeline.orchestrator.profile_parser_service.parse_style_profile",
        lambda request: StyleProfile(
            style_label=request.style_tone,
            emotion_label="平静理解",
            intensity_level="low",
            custom_notes=request.custom_style_text,
        ),
    )
    monkeypatch.setattr(
        "app.services.generation_pipeline.orchestrator.trend_strategy_service.get_template",
        lambda request, audience_profile: PlatformTrendTemplate(
            platform=request.target_platform,
            content_type=request.content_type,
            summary="适合结论先行与实用解释并行的节奏。",
            hook_patterns=["先说常见误区"],
            rhythm_patterns=["一句结论一句解释"],
            title_cover_style=["生活感标题", "低压但明确"],
            audience_preference_summary="更偏好被理解感和可执行建议。",
            avoid_patterns=["制造焦虑"],
            hot_topics_summary=["睡眠债", "情绪波动"],
            source_type="db_truth",
            updated_at="2026-03-27T00:00:00+00:00",
        ),
    )
    monkeypatch.setattr(
        "app.services.generation_pipeline.orchestrator.narrative_generator_service.build_narrative_bundle_result",
        lambda *args, **kwargs: NarrativeBundleResult(
            title="为什么一熬夜，整个人更容易烦躁？",
            one_sentence_summary="用一条更容易传播的结构解释睡眠与情绪的关系。",
            segments=[
                ScriptSegment(
                    segment_number=1,
                    segment_title="误区切入",
                    segment_goal="先建立共识",
                    narration="n",
                    subtitle_text="s",
                    visual_description="v",
                    emotion="平静理解",
                    rhythm="一句结论一句解释",
                )
            ],
            key_shots=[
                KeyShot(
                    shot_title="生活镜头",
                    shot_focus="地铁通勤疲惫瞬间",
                    shot_duration_seconds=4,
                    transition_hint="淡入正文",
                )
            ],
            title_alternatives=["熬夜后更烦躁，不只是你脾气变差"],
            hook_alternatives=["很多人的坏情绪，其实从缺觉那一刻就开始了"],
            title_candidates=[
                StructuredTextCandidate(
                    candidate_text="熬夜后更烦躁，不只是你脾气变差",
                    usage_scenario="结果页标题候选",
                    design_reason="用于保持 checkpoint 测试夹具与真实 schema 一致。",
                )
            ],
            hook_candidates=[
                StructuredTextCandidate(
                    candidate_text="很多人的坏情绪，其实从缺觉那一刻就开始了",
                    usage_scenario="结果页钩子候选",
                    design_reason="用于保持 checkpoint 测试夹具与真实 schema 一致。",
                )
            ],
            runtime=NarrativeGenerationRuntime(
                source_type="structured_output_gateway",
                fallback_reason=None,
            ),
        ),
    )


def test_generation_result_can_be_restored_from_latest_checkpoint(monkeypatch) -> None:
    reset_database()
    created = generation_pipeline_store.create(build_request())
    generation_pipeline_store.mark_ready_for_result(created.generation_id)
    record = generation_pipeline_store.get_record(created.generation_id)
    patch_generation_dependencies(monkeypatch)

    result = generation_execution_orchestrator.execute(record)
    saved_before_restore = generation_pipeline_store.result_repository.get(created.generation_id)
    restored = restore_generation_from_latest_checkpoint(created.generation_id)
    saved_after_restore = generation_pipeline_store.result_repository.get(created.generation_id)
    status_after_restore = generation_pipeline_store.get_status(created.generation_id)

    assert result.export_meta["generation_id"] == created.generation_id
    assert saved_before_restore is None
    assert restored.restored is True
    assert restored.status == "DONE"
    assert saved_after_restore is not None
    assert saved_after_restore.export_meta["generation_id"] == created.generation_id
    assert str(status_after_restore.status) == "DONE"
