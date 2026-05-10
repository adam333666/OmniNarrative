from __future__ import annotations

import pytest

from app.services.generation_pipeline.checkpointer import generation_checkpoint_service
from app.services.generation_pipeline.orchestrator import generation_execution_orchestrator
from app.services.generation_pipeline.runner import generation_execution_runner


@pytest.fixture(autouse=True)
def cleanup_generation_runtime_resources():
    yield
    generation_execution_runner.shutdown(wait=False)
    generation_execution_orchestrator.graph = None
    generation_checkpoint_service.reset()
