from pydantic import BaseModel, Field, field_validator

from app.schemas.narrative_package import KeyShot, ScriptSegment, StructuredTextCandidate


class StructuredNarrativeBundle(BaseModel):
    main_title: str = Field(description="成品主标题，适合目标平台分发。")
    one_sentence_summary: str = Field(description="一句话概括内容方案。")
    segments: list[ScriptSegment] = Field(description="结构化脚本段落，建议 3 到 5 段。")
    key_shots: list[KeyShot] = Field(description="关键镜头建议，建议 2 到 4 个。")
    title_alternatives: list[str] = Field(description="标题备选列表，至少 2 个。")
    hook_alternatives: list[str] = Field(description="开场钩子备选列表，至少 2 个。")
    title_candidates: list[StructuredTextCandidate] = Field(default_factory=list, description="结构化标题候选。")
    hook_candidates: list[StructuredTextCandidate] = Field(default_factory=list, description="结构化开场钩子候选。")

    @field_validator("main_title", "one_sentence_summary")
    @classmethod
    def _validate_non_empty_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("value must not be empty")
        return cleaned

    @field_validator("title_alternatives", "hook_alternatives")
    @classmethod
    def _validate_non_empty_items(cls, value: list[str]) -> list[str]:
        cleaned = [item.strip() for item in value if item.strip()]
        if len(cleaned) < 2:
            raise ValueError("at least two non-empty items are required")
        return cleaned

    @field_validator("segments")
    @classmethod
    def _validate_segments(cls, value: list[ScriptSegment]) -> list[ScriptSegment]:
        if len(value) < 3:
            raise ValueError("at least three segments are required")
        return value

    @field_validator("key_shots")
    @classmethod
    def _validate_key_shots(cls, value: list[KeyShot]) -> list[KeyShot]:
        if len(value) < 2:
            raise ValueError("at least two key shots are required")
        return value
