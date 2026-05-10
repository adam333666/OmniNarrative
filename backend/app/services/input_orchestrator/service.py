from fastapi import HTTPException

from app.schemas.creation_request import CreationRequest


class InputOrchestratorService:
    def normalize_and_validate(self, payload: CreationRequest) -> CreationRequest:
        normalized = payload.normalized()

        try:
            normalized.validate_enums()
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

        return normalized


input_orchestrator_service = InputOrchestratorService()
