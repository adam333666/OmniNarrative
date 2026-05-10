from __future__ import annotations

from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from app.core.enums import GenerationStatus
from app.schemas.generation import GenerationRecord
from app.schemas.narrative_package import KeyShot, ResultEnvelope, ScriptSegment, StructuredTextCandidate
from app.schemas.profiles import AudienceProfile, StyleProfile
from app.schemas.trend_template import PlatformTrendTemplate
from app.services.generation_pipeline.checkpointer import generation_checkpoint_service
from app.services.generation_pipeline.store import generation_pipeline_store
from app.services.narrative_generator.service import NarrativeGenerationRuntime, narrative_generator_service
from app.services.package_assembler.service import package_assembler_service
from app.services.profile_parser.service import profile_parser_service
from app.services.trend_strategy.service import trend_strategy_service


class GenerationExecutionState(TypedDict, total=False):
    generation_id: str
    record: GenerationRecord
    audience_profile: AudienceProfile
    style_profile: StyleProfile
    trend_summary: PlatformTrendTemplate
    title: str
    one_sentence_summary: str
    script_segments: list[ScriptSegment]
    key_shots: list[KeyShot]
    title_alternatives: list[str]
    hook_alternatives: list[str]
    title_candidates: list[StructuredTextCandidate]
    hook_candidates: list[StructuredTextCandidate]
    narrative_runtime: NarrativeGenerationRuntime
    result: ResultEnvelope


class GenerationExecutionOrchestrator:
    def __init__(self) -> None:
        self.graph = None

    def _build_graph(self):
        workflow = StateGraph(GenerationExecutionState)
        workflow.add_node("parse_profiles", self._parse_profiles)
        workflow.add_node("adapt_trend", self._adapt_trend)
        workflow.add_node("generate_narrative", self._generate_narrative)
        workflow.add_node("assemble_package", self._assemble_package)
        workflow.add_edge(START, "parse_profiles")
        workflow.add_edge("parse_profiles", "adapt_trend")
        workflow.add_edge("adapt_trend", "generate_narrative")
        workflow.add_edge("generate_narrative", "assemble_package")
        workflow.add_edge("assemble_package", END)
        return workflow.compile(checkpointer=generation_checkpoint_service.get_checkpointer())

    def _get_graph(self):
        if self.graph is None:
            self.graph = self._build_graph()
        return self.graph

    def execute(self, record: GenerationRecord) -> ResultEnvelope:
        try:
            final_state = self._get_graph().invoke(
                {
                    "generation_id": record.generation_id,
                    "record": record,
                },
                config={"configurable": {"thread_id": record.generation_id, "checkpoint_ns": "generation_execution"}},
            )
            return final_state["result"]
        except Exception as exc:
            generation_pipeline_store.mark_failed(
                record.generation_id,
                error_message=str(exc) or "Generation failed unexpectedly.",
            )
            raise

    def _parse_profiles(self, state: GenerationExecutionState) -> GenerationExecutionState:
        record = state["record"]
        generation_pipeline_store.mark_stage(
            record.generation_id,
            stage_status=GenerationStatus.profile_parsing,
            stage_message="正在抽取受众与风格标签",
        )
        return {
            "audience_profile": profile_parser_service.parse_audience_profile(record.request),
            "style_profile": profile_parser_service.parse_style_profile(record.request),
        }

    def _adapt_trend(self, state: GenerationExecutionState) -> GenerationExecutionState:
        record = state["record"]
        audience_profile = state["audience_profile"]
        generation_pipeline_store.mark_stage(
            record.generation_id,
            stage_status=GenerationStatus.trend_adapting,
            stage_message="正在进行平台与趋势适配",
        )
        return {
            "trend_summary": trend_strategy_service.get_template(record.request, audience_profile),
        }

    def _generate_narrative(self, state: GenerationExecutionState) -> GenerationExecutionState:
        record = state["record"]
        generation_pipeline_store.mark_stage(
            record.generation_id,
            stage_status=GenerationStatus.narrative_generating,
            stage_message="正在生成叙事骨架",
        )
        bundle_result = narrative_generator_service.build_narrative_bundle_result(
            record.request,
            state["audience_profile"],
            state["style_profile"],
            state["trend_summary"],
        )
        return {
            "title": bundle_result.title,
            "one_sentence_summary": bundle_result.one_sentence_summary,
            "script_segments": bundle_result.segments,
            "key_shots": bundle_result.key_shots,
            "title_alternatives": bundle_result.title_alternatives,
            "hook_alternatives": bundle_result.hook_alternatives,
            "title_candidates": bundle_result.title_candidates,
            "hook_candidates": bundle_result.hook_candidates,
            "narrative_runtime": bundle_result.runtime,
        }

    def _assemble_package(self, state: GenerationExecutionState) -> GenerationExecutionState:
        record = state["record"]
        generation_pipeline_store.mark_ready_for_result(record.generation_id)
        result = package_assembler_service.build_result(
            generation_id=record.generation_id,
            request=record.request,
            audience_profile=state["audience_profile"],
            style_profile=state["style_profile"],
            trend_summary=state["trend_summary"],
            title=state["title"],
            one_sentence_summary=state["one_sentence_summary"],
            script_segments=state["script_segments"],
            key_shots=state["key_shots"],
            title_alternatives=state["title_alternatives"],
            hook_alternatives=state["hook_alternatives"],
            title_candidates=state["title_candidates"],
            hook_candidates=state["hook_candidates"],
            narrative_runtime={
                "source_type": state["narrative_runtime"].source_type,
                "fallback_reason": state["narrative_runtime"].fallback_reason,
            },
        )
        return {"result": result}


generation_execution_orchestrator = GenerationExecutionOrchestrator()
