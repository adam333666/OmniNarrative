from __future__ import annotations

import os
from pathlib import Path

TEST_DB_PATH = Path("/tmp/multi_media_test.db")
os.environ.setdefault("DATABASE_URL", f"sqlite+pysqlite:///{TEST_DB_PATH}")

from app.db.bootstrap import bootstrap_database
from app.db.repositories.generation_job_event_repository import SqlAlchemyGenerationJobEventRepository
from app.db.repositories.generation_job_repository import SqlAlchemyGenerationJobRepository
from app.db.repositories.generation_result_repository import SqlAlchemyGenerationResultRepository
from app.db.session import get_engine, get_session_factory
from app.schemas.creation_request import CreationRequest
from app.schemas.narrative_package import KeyShot, ResultEnvelope, ScriptSegment, StructuredTextCandidate
from app.schemas.profiles import AudienceProfile, StyleProfile
from app.schemas.trend_template import PlatformTrendTemplate
from app.services.generation_pipeline.orchestrator import generation_execution_orchestrator
from app.services.generation_pipeline.result_builder import generation_result_builder
from app.services.generation_pipeline.runner import generation_execution_runner
from app.services.generation_pipeline.store import generation_pipeline_store
from app.services.narrative_generator.service import NarrativeBundleResult, NarrativeGenerationRuntime


def reset_database() -> None:
    get_engine().dispose()
    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink()
    get_engine.cache_clear()
    get_session_factory.cache_clear()
    generation_execution_runner.shutdown(wait=False)
    bootstrap_database()
    generation_pipeline_store.repository = SqlAlchemyGenerationJobRepository()
    generation_pipeline_store.result_repository = SqlAlchemyGenerationResultRepository()
    generation_pipeline_store.event_repository = SqlAlchemyGenerationJobEventRepository()
    generation_result_builder.result_repository = SqlAlchemyGenerationResultRepository()


def build_request() -> CreationRequest:
    return CreationRequest(
        theme_text="时间旅行悖论",
        content_type="science_popularization",
        target_platform="bilibili",
        target_audience_text="18到28岁，喜欢科幻设定和逻辑推理的观众",
        style_tone="suspense",
        custom_style_text="保持一点烧脑感",
    )


def build_result(generation_id: str) -> ResultEnvelope:
    return ResultEnvelope.model_validate(
        {
            "request_summary": {"theme_text": "时间旅行悖论"},
            "analysis": {
                "audience_profile": {
                    "raw_text": "x",
                    "age_group_guess": "18-24",
                    "interest_tags": ["脑洞设定"],
                    "pain_points": ["复杂概念理解门槛高"],
                    "content_preference": ["开头要快"],
                    "emotion_preference": ["希望被带入但不被说教"],
                },
                "style_profile": {
                    "style_label": "suspense",
                    "emotion_label": "紧张好奇",
                    "intensity_level": "medium",
                    "custom_notes": None,
                },
                "trend_summary": {
                    "platform": "bilibili",
                    "content_type": "science_popularization",
                    "summary": "平台节奏偏强钩子",
                    "hook_patterns": ["先抛问题"],
                    "rhythm_patterns": ["快切进入"],
                    "title_cover_style": "高信息密度",
                    "avoid_patterns": ["铺垫过长"],
                    "source_type": "db_truth",
                    "updated_at": "2026-03-27T00:00:00+00:00",
                },
                "key_design_decisions": ["先完整后优化"],
                "runtime_diagnostics": {
                    "narrative_generation": {"source_type": "structured_output_gateway", "fallback_reason": None},
                    "package_assembly": {"source_type": "structured_output_gateway", "fallback_reason": None},
                },
            },
            "result_package": {
                "overview": {
                    "main_title": "时间旅行悖论，为什么会让人越想越上头？",
                },
                "script_layer": {"segments": [], "key_shots": []},
                "multimodal_layer": {},
                "platform_layer": {},
                "machine_payload_layer": {},
            },
            "export_meta": {
                "schema_version": "0.1.0",
                "generation_id": generation_id,
                "generated_at": "2026-03-27T00:00:00+00:00",
            },
        }
    )


def test_generation_orchestrator_executes_stages_in_order(monkeypatch) -> None:
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
            title_candidates=[
                StructuredTextCandidate(
                    candidate_text="标题备选",
                    usage_scenario="结果页标题候选",
                    design_reason="用于保持测试夹具与真实 schema 一致。",
                )
            ],
            hook_candidates=[
                StructuredTextCandidate(
                    candidate_text="钩子备选",
                    usage_scenario="结果页钩子候选",
                    design_reason="用于保持测试夹具与真实 schema 一致。",
                )
            ],
            runtime=NarrativeGenerationRuntime(source_type="structured_output_gateway", fallback_reason=None),
        ),
    )
    monkeypatch.setattr(
        "app.services.generation_pipeline.orchestrator.package_assembler_service.build_result",
        lambda **kwargs: build_result(kwargs["generation_id"]),
    )

    result = generation_execution_orchestrator.execute(record)
    events = generation_pipeline_store.list_events(created.generation_id)

    assert result.export_meta["generation_id"] == created.generation_id
    assert [event.event_type for event in events] == [
        "CREATED",
        "READY_FOR_RESULT",
        "STAGE_UPDATED",
        "STAGE_UPDATED",
        "STAGE_UPDATED",
        "READY_FOR_RESULT",
    ]
    assert [event.stage for event in events[-4:]] == [
        "PROFILE_PARSING",
        "TREND_ADAPTING",
        "NARRATIVE_GENERATING",
        "PACKAGE_ASSEMBLING",
    ]


def test_generation_orchestrator_marks_failed_when_step_raises(monkeypatch) -> None:
    reset_database()
    created = generation_pipeline_store.create(build_request())
    generation_pipeline_store.mark_ready_for_result(created.generation_id)
    record = generation_pipeline_store.get_record(created.generation_id)

    monkeypatch.setattr(
        "app.services.generation_pipeline.orchestrator.profile_parser_service.parse_audience_profile",
        lambda request: (_ for _ in ()).throw(RuntimeError("forced parser failure")),
    )

    try:
        generation_execution_orchestrator.execute(record)
    except RuntimeError as exc:
        assert str(exc) == "forced parser failure"
    else:
        raise AssertionError("Expected orchestrator failure to bubble up")

    status = generation_pipeline_store.get_status(created.generation_id)
    events = generation_pipeline_store.list_events(created.generation_id)

    assert status.status == "FAILED"
    assert status.current_stage == "PROFILE_PARSING"
    assert status.error_message == "forced parser failure"
    assert events[-1].event_type == "FAILED"


def test_background_runner_records_crash_event_when_materialization_crashes(monkeypatch) -> None:
    reset_database()
    created = generation_pipeline_store.create(build_request())

    monkeypatch.setattr(
        "app.services.generation_pipeline.runner.generation_materialization_coordinator.materialize",
        lambda generation_id, allow_pending_start: (_ for _ in ()).throw(RuntimeError("forced background crash")),
    )

    try:
        generation_execution_runner._run(created.generation_id)
    except RuntimeError as exc:
        assert str(exc) == "forced background crash"
    else:
        raise AssertionError("Expected background runner crash to bubble up")

    status = generation_pipeline_store.get_status(created.generation_id)
    events = generation_pipeline_store.list_events(created.generation_id)

    assert status.status == "FAILED"
    assert status.error_message == "forced background crash"
    assert events[-2].event_type == "FAILED"
    assert events[-1].event_type == "BACKGROUND_CRASHED"
