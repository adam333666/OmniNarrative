from pydantic import BaseModel, Field


class VideoGenerationPayload(BaseModel):
    video_meta: dict
    segments: list[dict]
    shots: list[dict]
    characters: list[str]
    scenes: list[str]
    scene_progression: list[str]
    motion_cues: list[str]
    asset_props: list[str]
    visual_references: list[str]
    style_constraints: list[str]
    subtitle_blocks: list[str]
    audio_guides: list[str]
    negative_constraints: list[str]
    publish_timing_suggestions: list[str]
    distribution_angles: list[str]
    thumbnail_copy_candidates: list[str]
    comment_guidance: list[str]
    cover_copy_alternatives: list[str]
    title_alternatives: list[str]
    hook_alternatives: list[str]
    title_candidates: list[dict]
    hook_candidates: list[dict]
    cover_candidates: list[dict]
    distribution_angle_candidates: list[dict]
    editing_checklist: list[str]
    cta_variants: list[str]
    storyboard_beats: list[str]
    storyboard_frames: list[dict]
    asset_preparation_notes: list[dict]
    voiceover_subtitle_alignment: list[dict]
    estimated_total_duration_seconds: int
    runtime_pacing_notes: list[str]
    trend_source_trace: list[dict]
    overview_expansion: dict = Field(default_factory=dict)
    analysis_expansion: dict = Field(default_factory=dict)
    expanded_segments: list[dict] = Field(default_factory=list)
    expanded_key_shots: list[dict] = Field(default_factory=list)
    title_strategy_notes: list[dict] = Field(default_factory=list)
    hook_strategy_notes: list[dict] = Field(default_factory=list)
    retention_design_notes: list[dict] = Field(default_factory=list)
    multimodal_expansion: dict = Field(default_factory=dict)
    platform_expansion: dict = Field(default_factory=dict)
    machine_payload_expansion: dict = Field(default_factory=dict)
    quality_control_notes: list[str] = Field(default_factory=list)
