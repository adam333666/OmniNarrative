from datetime import datetime

from fastapi import APIRouter, Header, HTTPException, Query
from fastapi.responses import PlainTextResponse

from app.schemas.creation_request import CreationRequest
from app.core.config import settings
from app.db.repositories.generation_result_repository import SqlAlchemyGenerationResultRepository
from app.schemas.generation import GenerationCreateResponse, GenerationDiagnosticsResponse, GenerationEventItem
from app.schemas.narrative_package import ResultEnvelope
from app.schemas.status import GenerationStatusResponse
from app.schemas.video_payload import VideoGenerationPayload
from app.services.export_payload.service import export_payload_service
from app.services.generation_pipeline.runner import generation_execution_runner
from app.services.generation_pipeline.result_builder import generation_result_builder
from app.services.generation_pipeline.store import generation_pipeline_store
from app.services.input_orchestrator.service import input_orchestrator_service

router = APIRouter(prefix="/creations", tags=["creations"])


@router.post("/generate", response_model=GenerationCreateResponse)
def generate_creation(payload: CreationRequest) -> GenerationCreateResponse:
    if not settings.generation_auto_start_enabled:
        raise HTTPException(
            status_code=503,
            detail="Generation auto-start is disabled in the current environment",
        )
    normalized = input_orchestrator_service.normalize_and_validate(payload)
    record = generation_pipeline_store.create(normalized)
    try:
        submitted = generation_execution_runner.submit(record.generation_id)
    except Exception as exc:
        generation_pipeline_store.mark_failed(
            record.generation_id,
            error_message=str(exc) or "Generation could not be scheduled for background execution",
        )
        raise HTTPException(
            status_code=503,
            detail="Generation could not be scheduled for background execution",
        ) from exc
    if not submitted:
        generation_pipeline_store.mark_failed(
            record.generation_id,
            error_message="Generation could not be scheduled for background execution",
        )
        raise HTTPException(status_code=503, detail="Generation could not be scheduled for background execution")
    return GenerationCreateResponse(
        generation_id=record.generation_id,
        current_status=record.current_status,
        created_at=record.created_at,
    )


@router.get("/{generation_id}/status", response_model=GenerationStatusResponse)
def get_generation_status(generation_id: str) -> GenerationStatusResponse:
    return generation_pipeline_store.get_status(generation_id)


@router.get("/{generation_id}/result", response_model=ResultEnvelope)
def get_generation_result(generation_id: str) -> ResultEnvelope:
    return generation_result_builder.build(generation_id)


@router.get("/{generation_id}/export/json", response_model=ResultEnvelope)
def export_generation_json(generation_id: str) -> ResultEnvelope:
    return generation_result_builder.build(generation_id)


@router.get("/{generation_id}/export/md", response_class=PlainTextResponse)
def export_generation_markdown(generation_id: str) -> str:
    result = generation_result_builder.build(generation_id)
    return export_payload_service.build_markdown(result)


@router.get("/{generation_id}/video-payload", response_model=VideoGenerationPayload)
def export_video_payload(generation_id: str) -> VideoGenerationPayload:
    result = generation_result_builder.build(generation_id)
    return export_payload_service.build_video_payload(result)


@router.get("/{generation_id}/diagnostics", response_model=GenerationDiagnosticsResponse)
def get_generation_diagnostics(
    generation_id: str,
    event_type: str | None = Query(default=None),
    limit: int | None = Query(default=None, ge=1, le=200),
    since: datetime | None = Query(default=None),
    until: datetime | None = Query(default=None),
    failed_only: bool = Query(default=False),
    x_internal_api_key: str = Header(default="", alias="X-Internal-Api-Key"),
) -> GenerationDiagnosticsResponse:
    if not settings.internal_api_key:
        raise HTTPException(status_code=503, detail="Diagnostics endpoint is not enabled in the current environment")
    if x_internal_api_key != settings.internal_api_key:
        raise HTTPException(status_code=403, detail="Invalid internal API key")

    status_snapshot = generation_pipeline_store.get_status(generation_id)
    events = [
        GenerationEventItem(
            generation_id=item.generation_id,
            event_type=item.event_type,
            status=item.status,
            stage=item.stage,
            stage_message=item.stage_message,
            error_message=item.error_message,
            occurred_at=item.occurred_at,
        )
        for item in generation_pipeline_store.list_events(
            generation_id,
            event_type=event_type,
            limit=limit,
            since=since,
            until=until,
            failed_only=failed_only,
        )
    ]
    return GenerationDiagnosticsResponse(
        generation_id=generation_id,
        status_snapshot=status_snapshot,
        has_result_snapshot=SqlAlchemyGenerationResultRepository().get(generation_id) is not None,
        event_count=len(events),
        events=events,
    )
