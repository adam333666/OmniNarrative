from datetime import datetime

from pydantic import BaseModel

from app.schemas.creation_request import CreationRequest
from app.schemas.status import GenerationStatusResponse


class GenerationCreateResponse(BaseModel):
    generation_id: str
    current_status: str
    created_at: datetime


class GenerationRecord(BaseModel):
    generation_id: str
    request: CreationRequest
    created_at: datetime
    current_status: str
    current_stage: str
    stage_message: str
    failed: bool = False
    timed_out: bool = False
    failure_reason: str | None = None
    completed_at: datetime | None = None
    updated_at: datetime | None = None


class GenerationEventItem(BaseModel):
    generation_id: str
    event_type: str
    status: str
    stage: str
    stage_message: str
    error_message: str | None
    occurred_at: datetime


class GenerationDiagnosticsResponse(BaseModel):
    generation_id: str
    status_snapshot: GenerationStatusResponse
    has_result_snapshot: bool
    event_count: int
    events: list[GenerationEventItem]


class GenerationCheckpointItem(BaseModel):
    checkpoint_id: str | None
    checkpoint_ns: str
    thread_id: str | None
    created_at: str | None
    channel_keys: list[str]
    metadata: dict
    pending_write_count: int


class GenerationCheckpointListResponse(BaseModel):
    generation_id: str
    total: int
    items: list[GenerationCheckpointItem]


class GenerationCheckpointRestoreResponse(BaseModel):
    generation_id: str
    restored: bool
    status: str
    result_generated_at: str


class GenerationFailureAttribution(BaseModel):
    category: str
    stage: str | None
    stage_message: str | None
    latest_event_type: str | None
    latest_error_message: str | None
    recovery_hint: str
    can_restore_result_snapshot: bool


class GenerationCheckpointStateResponse(BaseModel):
    generation_id: str
    checkpoint_id: str | None
    checkpoint_ns: str
    thread_id: str | None
    created_at: str | None
    channel_keys: list[str]
    metadata: dict
    has_result: bool
    result_title: str | None
    result_summary: str | None
    script_segment_count: int
    failure_attribution: GenerationFailureAttribution
