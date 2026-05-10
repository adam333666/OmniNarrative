from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.schemas.profiles import AudienceProfile, StyleProfile
from app.schemas.trend_template import PlatformTrendTemplate


class StructuredTextCandidate(BaseModel):
    candidate_text: str
    usage_scenario: str = ""
    design_reason: str = ""


class ExpansionDetailItem(BaseModel):
    title: str
    detail: str
    purpose: str = ""
    execution_hint: str = ""


class StoryboardFrame(BaseModel):
    beat_number: int
    beat_title: str
    linked_segment_number: int
    linked_key_shot_title: str = ""
    visual_focus: str
    narration_focus: str
    estimated_duration_seconds: int
    asset_requirement: str
    editing_note: str


class AssetPreparationItem(BaseModel):
    item_name: str
    linked_beat_number: int
    requirement_detail: str
    ready_stage: str


class VoiceoverSubtitleAlignmentItem(BaseModel):
    linked_beat_number: int
    voiceover_line: str
    subtitle_line: str
    timing_note: str


class ScriptSegment(BaseModel):
    segment_number: int
    segment_title: str
    segment_goal: str
    narration: str
    subtitle_text: str
    visual_description: str
    emotion: str
    rhythm: str


class KeyShot(BaseModel):
    shot_title: str
    shot_focus: str
    shot_duration_seconds: int
    transition_hint: str
    camera_movement: str = ""
    transition_style: str = ""
    asset_dependency: str = ""
    voiceover_cue: str = ""


class ExpandedScriptSegment(BaseModel):
    segment_number: int
    narrative_function: str
    expansion_goal: str
    transition_in: str
    transition_out: str
    audience_psychology: str
    detail_outline: list[str]
    delivery_notes: list[str]
    alt_narration_lines: list[str]
    visual_layers: list[str]


class ExpandedKeyShot(BaseModel):
    shot_title: str
    narrative_role: str
    composition_notes: str
    motion_design: str
    asset_layers: list[str]
    edit_variants: list[str]
    failure_fallback: str


class OverviewLayer(BaseModel):
    main_title: str
    one_sentence_summary: str
    content_positioning: str
    target_platform: str
    target_audience_summary: str
    style_summary: str
    design_summary: str


class ScriptLayer(BaseModel):
    segments: list[ScriptSegment]
    key_shots: list[KeyShot]
    script_note: str
    title_alternatives: list[str]
    hook_alternatives: list[str]
    title_candidates: list[StructuredTextCandidate] = Field(default_factory=list)
    hook_candidates: list[StructuredTextCandidate] = Field(default_factory=list)


class MultimodalLayer(BaseModel):
    characters: list[str]
    scenes: list[str]
    visual_style: str
    subtitle_style: str
    audio_guides: list[str]
    visual_keywords: list[str]
    rhythm_guidance: list[str]
    scene_progression: list[str]
    motion_cues: list[str]
    asset_props: list[str]
    visual_references: list[str]


class PlatformLayer(BaseModel):
    platform_strategy: str
    trend_summary: PlatformTrendTemplate
    audience_adaptation: str
    hook_design_reason: str
    rhythm_structure_reason: str
    title_cover_style: list[str]
    publishing_copy_suggestion: str
    avoid_patterns: list[str]
    cover_copy_alternatives: list[str]
    comment_guidance: list[str]
    publish_timing_suggestions: list[str]
    distribution_angles: list[str]
    thumbnail_copy_candidates: list[str]
    cover_candidates: list[StructuredTextCandidate] = Field(default_factory=list)
    distribution_angle_candidates: list[StructuredTextCandidate] = Field(default_factory=list)


class MachinePayloadLayer(BaseModel):
    video_prompt_block: str
    character_consistency_block: str
    scene_description_block: str
    style_constraints: list[str]
    negative_constraints: list[str]
    key_shot_prompts: list[str]
    shot_duration_suggestions: list[int]
    thumbnail_prompt_block: str
    voiceover_prompt_block: str
    asset_checklist: list[str]
    editing_checklist: list[str]
    cta_variants: list[str]
    storyboard_beats: list[str] = Field(default_factory=list)
    storyboard_frames: list[StoryboardFrame] = Field(default_factory=list)
    asset_preparation_notes: list[AssetPreparationItem] = Field(default_factory=list)
    voiceover_subtitle_alignment: list[VoiceoverSubtitleAlignmentItem] = Field(default_factory=list)
    estimated_total_duration_seconds: int = 0
    runtime_pacing_notes: list[str] = Field(default_factory=list)


class OverviewExpansion(BaseModel):
    positioning_rationale: list[ExpansionDetailItem]
    audience_value_points: list[ExpansionDetailItem]
    execution_priorities: list[ExpansionDetailItem]
    risk_controls: list[ExpansionDetailItem]


class AnalysisExpansion(BaseModel):
    audience_mindset_layers: list[ExpansionDetailItem]
    comprehension_barriers: list[ExpansionDetailItem]
    emotional_triggers: list[ExpansionDetailItem]
    trend_application_notes: list[ExpansionDetailItem]


class ScriptExpansion(BaseModel):
    expanded_segments: list[ExpandedScriptSegment]
    expanded_key_shots: list[ExpandedKeyShot]
    title_strategy_notes: list[ExpansionDetailItem]
    hook_strategy_notes: list[ExpansionDetailItem]
    retention_design_notes: list[ExpansionDetailItem]


class MultimodalExpansion(BaseModel):
    scene_blueprints: list[ExpansionDetailItem]
    visual_motif_notes: list[ExpansionDetailItem]
    audio_layering_notes: list[ExpansionDetailItem]
    asset_pipeline_notes: list[ExpansionDetailItem]


class PlatformExpansion(BaseModel):
    publishing_playbook: list[ExpansionDetailItem]
    comment_thread_playbook: list[StructuredTextCandidate]
    cover_iteration_notes: list[ExpansionDetailItem]
    series_extension_angles: list[StructuredTextCandidate]
    release_rhythm_notes: list[ExpansionDetailItem]


class MachinePayloadExpansion(BaseModel):
    production_phases: list[ExpansionDetailItem]
    shot_execution_notes: list[ExpandedKeyShot]
    subtitle_strategy_notes: list[ExpansionDetailItem]
    qa_checkpoints: list[ExpansionDetailItem]
    fallback_actions: list[str]


class StructuredPackageScaffold(BaseModel):
    overview: OverviewLayer
    multimodal_layer: MultimodalLayer
    platform_layer: PlatformLayer
    machine_payload_layer: MachinePayloadLayer
    key_design_decisions: list[str] = Field(min_length=2, max_length=4)


class ExpandedPackageScaffold(BaseModel):
    overview_expansion: OverviewExpansion
    analysis_expansion: AnalysisExpansion
    script_expansion: ScriptExpansion
    multimodal_expansion: MultimodalExpansion
    platform_expansion: PlatformExpansion
    machine_payload_expansion: MachinePayloadExpansion
    quality_control_notes: list[str] = Field(min_length=3, max_length=6)


class NarrativePackage(BaseModel):
    overview: dict[str, Any]
    script_layer: dict[str, Any]
    multimodal_layer: dict[str, Any]
    platform_layer: dict[str, Any]
    machine_payload_layer: dict[str, Any]


class ResultEnvelope(BaseModel):
    request_summary: dict[str, Any]
    analysis: dict[str, Any]
    result_package: NarrativePackage
    export_meta: dict[str, Any]


class ResultBuildArtifacts(BaseModel):
    audience_profile: AudienceProfile
    style_profile: StyleProfile
    trend_summary: PlatformTrendTemplate
    script_segments: list[ScriptSegment]
    key_shots: list[KeyShot]
    generated_at: datetime
