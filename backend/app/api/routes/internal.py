from fastapi import APIRouter, Depends, Query

from app.api.deps import require_internal_api_key
from app.schemas.generation import (
    GenerationCheckpointItem,
    GenerationCheckpointListResponse,
    GenerationCheckpointRestoreResponse,
    GenerationCheckpointStateResponse,
)
from app.schemas.trend_template import InternalTrendSummaryResponse, TrendRefreshResponse
from app.services.generation_pipeline.checkpointer import generation_checkpoint_service
from app.services.generation_pipeline.recovery import generation_checkpoint_recovery_service
from app.services.generation_pipeline.store import generation_pipeline_store
from app.services.trend_strategy.service import trend_strategy_service

router = APIRouter(
    prefix="/internal",
    tags=["internal"],
    dependencies=[Depends(require_internal_api_key)],
)


@router.post("/trend-refresh", response_model=TrendRefreshResponse)
def refresh_internal_trends() -> TrendRefreshResponse:
    return trend_strategy_service.refresh_templates()


@router.get("/trend-summary/{platform}", response_model=InternalTrendSummaryResponse)
def get_platform_trend_summary(
    platform: str,
    content_type: str | None = Query(default=None),
) -> InternalTrendSummaryResponse:
    return trend_strategy_service.get_platform_summary(platform=platform, content_type=content_type)


@router.get("/generation-checkpoints/{generation_id}", response_model=GenerationCheckpointListResponse)
def get_generation_checkpoints(
    generation_id: str,
    limit: int = Query(default=20, ge=1, le=100),
) -> GenerationCheckpointListResponse:
    generation_pipeline_store.get_record(generation_id)
    items = [
        GenerationCheckpointItem.model_validate(item)
        for item in generation_checkpoint_service.list_checkpoints(generation_id, limit=limit)
    ]
    return GenerationCheckpointListResponse(
        generation_id=generation_id,
        total=len(items),
        items=items,
    )


@router.get("/generation-checkpoints/{generation_id}/latest-state", response_model=GenerationCheckpointStateResponse)
def get_generation_latest_checkpoint_state(generation_id: str) -> GenerationCheckpointStateResponse:
    generation_pipeline_store.get_record(generation_id)
    state = generation_checkpoint_service.get_latest_checkpoint_state(generation_id)
    if state is None:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="No checkpoint state found for generation")
    return GenerationCheckpointStateResponse(
        generation_id=generation_id,
        **state,
    )


@router.post("/generation-checkpoints/{generation_id}/restore-latest", response_model=GenerationCheckpointRestoreResponse)
def restore_generation_from_latest_checkpoint(generation_id: str) -> GenerationCheckpointRestoreResponse:
    result = generation_checkpoint_recovery_service.restore_latest_result(generation_id)
    status = generation_pipeline_store.get_status(generation_id)
    status_value = status.status.value if hasattr(status.status, "value") else str(status.status)
    return GenerationCheckpointRestoreResponse(
        generation_id=generation_id,
        restored=True,
        status=status_value,
        result_generated_at=result.export_meta["generated_at"],
    )
