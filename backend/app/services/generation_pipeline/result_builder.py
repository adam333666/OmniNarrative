from app.db.repositories.generation_result_repository import SqlAlchemyGenerationResultRepository
from app.services.generation_pipeline.coordinator import generation_materialization_coordinator


class GenerationResultBuilder:
    def __init__(self, result_repository: SqlAlchemyGenerationResultRepository | None = None) -> None:
        self.result_repository = result_repository or SqlAlchemyGenerationResultRepository()
        generation_materialization_coordinator.result_repository = self.result_repository

    def build(self, generation_id: str):
        generation_materialization_coordinator.result_repository = self.result_repository
        return generation_materialization_coordinator.materialize(
            generation_id,
            allow_pending_start=False,
        )


generation_result_builder = GenerationResultBuilder()
