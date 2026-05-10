from __future__ import annotations

import os
from pathlib import Path
from types import SimpleNamespace

import pytest

TEST_DB_PATH = Path("/tmp/multi_media_test.db")
TEST_CHECKPOINT_PATH = Path("/tmp/multi_media_langgraph_checkpoint_test.sqlite")
os.environ.setdefault("DATABASE_URL", f"sqlite+pysqlite:///{TEST_DB_PATH}")

from app.api.routes.internal import get_generation_latest_checkpoint_state
from fastapi import HTTPException
from app.db.bootstrap import bootstrap_database
from app.db.repositories.generation_job_event_repository import SqlAlchemyGenerationJobEventRepository
from app.db.repositories.generation_job_repository import SqlAlchemyGenerationJobRepository
from app.db.repositories.generation_result_repository import SqlAlchemyGenerationResultRepository
from app.db.session import get_engine, get_session_factory
from app.schemas.creation_request import CreationRequest
from app.schemas.generation import GenerationRecord
from app.schemas.narrative_package import KeyShot, ScriptSegment
from app.schemas.narrative_package import StructuredTextCandidate
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
        theme_text="职场表达为什么容易被误解",
        content_type="knowledge_share",
        target_platform="bilibili",
        target_audience_text="刚进入职场，想提升表达效率的年轻人",
        style_tone="clear",
        custom_style_text="希望语言干脆一点",
    )


def patch_generation_dependencies(monkeypatch) -> None:
    monkeypatch.setattr(
        "app.services.generation_pipeline.orchestrator.profile_parser_service.parse_audience_profile",
        lambda request: AudienceProfile(
            raw_text=request.target_audience_text,
            age_group_guess="22-26",
            interest_tags=["表达能力"],
            pain_points=["明明说了很多却没有被理解"],
            content_preference=["案例式拆解"],
            emotion_preference=["希望直接获得有效建议"],
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
            summary="适合高信息密度和案例快切。",
            hook_patterns=["先说反常识结论"],
            rhythm_patterns=["问题-误区-解法"],
            title_cover_style=["强结论标题", "案例感封面"],
            audience_preference_summary="更偏好立即可用的表达框架。",
            avoid_patterns=["空泛鸡汤"],
            hot_topics_summary=["表达误区", "沟通效率"],
            source_type="db_truth",
            updated_at="2026-03-27T00:00:00+00:00",
        ),
    )
    monkeypatch.setattr(
        "app.services.generation_pipeline.orchestrator.narrative_generator_service.build_narrative_bundle_result",
        lambda *args, **kwargs: NarrativeBundleResult(
            title="为什么你说得很认真，别人却总是没听懂？",
            one_sentence_summary="把职场表达中的误区拆成一条更容易执行的脚本。",
            segments=[
                ScriptSegment(
                    segment_number=1,
                    segment_title="误区点名",
                    segment_goal="建立共鸣",
                    narration="n1",
                    subtitle_text="s1",
                    visual_description="v1",
                    emotion="直接清楚",
                    rhythm="问题-误区-解法",
                ),
                ScriptSegment(
                    segment_number=2,
                    segment_title="解决方案",
                    segment_goal="给出方法",
                    narration="n2",
                    subtitle_text="s2",
                    visual_description="v2",
                    emotion="直接清楚",
                    rhythm="问题-误区-解法",
                ),
            ],
            key_shots=[
                KeyShot(
                    shot_title="开场误区",
                    shot_focus="会议发言被打断",
                    shot_duration_seconds=4,
                    transition_hint="快切",
                )
            ],
            title_alternatives=["不是你不会说，是你说法太散"],
            hook_alternatives=["很多人表达无效，不是内容不够，而是结构不对"],
            title_candidates=[
                StructuredTextCandidate(
                    candidate_text="不是你不会说，是你说法太散",
                    usage_scenario="B站标题备选",
                    design_reason="强调问题切口，适合高信息密度表达。",
                )
            ],
            hook_candidates=[
                StructuredTextCandidate(
                    candidate_text="很多人表达无效，不是内容不够，而是结构不对",
                    usage_scenario="开场钩子备选",
                    design_reason="直接指出误区，便于迅速建立共鸣。",
                )
            ],
            runtime=NarrativeGenerationRuntime(
                source_type="structured_output_gateway",
                fallback_reason=None,
            ),
        ),
    )


def test_generation_latest_checkpoint_state_snapshot(monkeypatch) -> None:
    reset_database()
    created = generation_pipeline_store.create(build_request())
    generation_pipeline_store.mark_ready_for_result(created.generation_id)
    record = generation_pipeline_store.get_record(created.generation_id)
    patch_generation_dependencies(monkeypatch)

    generation_execution_orchestrator.execute(record)
    snapshot = get_generation_latest_checkpoint_state(created.generation_id)

    assert snapshot.generation_id == created.generation_id
    assert snapshot.has_result is True
    assert snapshot.result_title == "为什么你说得很认真，别人却总是没听懂？"
    assert snapshot.script_segment_count == 2
    assert "result" in snapshot.channel_keys
    assert snapshot.failure_attribution.category == "not_failed"
    assert snapshot.failure_attribution.can_restore_result_snapshot is True


def test_generation_latest_checkpoint_state_requires_existing_generation() -> None:
    reset_database()

    with pytest.raises(HTTPException) as exc_info:
        get_generation_latest_checkpoint_state("missing-generation")

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Generation not found"


def test_generation_latest_checkpoint_state_includes_failure_attribution(monkeypatch) -> None:
    generation_checkpoint_service.reset(sqlite_path=TEST_CHECKPOINT_PATH)

    fake_checkpoint_tuple = SimpleNamespace(
        config={"configurable": {"checkpoint_id": "cp_failed", "checkpoint_ns": "generation_execution", "thread_id": "gen_failed"}},
        checkpoint={"ts": "2026-03-30T14:30:00+00:00", "channel_values": {"analysis": {"ok": True}}},
        metadata={"step": "package_assembling"},
    )

    class FakeCheckpointer:
        def get_tuple(self, config: dict) -> SimpleNamespace:
            return fake_checkpoint_tuple

    monkeypatch.setattr(generation_checkpoint_service, "get_checkpointer", lambda: FakeCheckpointer())
    monkeypatch.setattr(
        "app.services.generation_pipeline.store.generation_pipeline_store.get_record",
        lambda generation_id: GenerationRecord(
                generation_id=generation_id,
                request=build_request(),
                created_at="2026-03-30T14:00:00+00:00",
                current_status="FAILED",
                current_stage="package_assembling",
                stage_message="在正在组装多模态内容包阶段失败",
                failure_reason="Structured output parsing exploded.",
            updated_at="2026-03-30T14:30:00+00:00",
            failed=True,
        ),
    )
    monkeypatch.setattr(
        "app.services.generation_pipeline.store.generation_pipeline_store.list_events",
        lambda generation_id, limit=20: [
            SimpleNamespace(
                generation_id=generation_id,
                event_type="BACKGROUND_STARTED",
                status="running",
                stage="package_assembling",
                stage_message="正在组装多模态内容包",
                error_message=None,
                occurred_at="2026-03-30T14:20:00+00:00",
            ),
            SimpleNamespace(
                generation_id=generation_id,
                event_type="FAILED",
                status="failed",
                stage="package_assembling",
                stage_message="在正在组装多模态内容包阶段失败",
                error_message="Structured output parsing exploded.",
                occurred_at="2026-03-30T14:30:00+00:00",
            ),
        ],
    )

    snapshot = generation_checkpoint_service.get_latest_checkpoint_state("gen_failed")

    assert snapshot is not None
    assert snapshot["failure_attribution"].category == "execution_failed"
    assert snapshot["failure_attribution"].latest_event_type == "FAILED"
    assert snapshot["failure_attribution"].can_restore_result_snapshot is False
