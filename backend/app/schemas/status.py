from datetime import datetime

from pydantic import BaseModel


class GenerationStatusResponse(BaseModel):
    generation_id: str
    status: str
    current_stage: str
    stage_message: str
    error_message: str | None = None
    created_at: datetime
    updated_at: datetime | None = None
    completed_at: datetime | None = None
    total_elapsed_seconds: int | None = None
    stage_elapsed_seconds: int | None = None
