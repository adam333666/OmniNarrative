from __future__ import annotations

import sqlite3
from pathlib import Path

from app.core.config import settings
from app.core.enums import GenerationStatus
from app.db.repositories.generation_job_event_repository import GenerationJobEventRecord
from app.schemas.generation import GenerationFailureAttribution
from app.schemas.narrative_package import ResultEnvelope
from app.integrations.langgraph_checkpoint_sqlite import SqliteSaver


class GenerationCheckpointService:
    def __init__(self, sqlite_path: Path | None = None) -> None:
        self.sqlite_path = sqlite_path or settings.generation_checkpoint_sqlite_path
        self._checkpointer: SqliteSaver | None = None

    def get_checkpointer(self) -> SqliteSaver:
        if self._checkpointer is None:
            self.sqlite_path.parent.mkdir(parents=True, exist_ok=True)
            connection = sqlite3.connect(str(self.sqlite_path), check_same_thread=False)
            self._checkpointer = SqliteSaver(connection)
            self._checkpointer.setup()
        return self._checkpointer

    def reset(self, *, sqlite_path: Path | None = None) -> None:
        if self._checkpointer is not None:
            self._checkpointer.conn.close()
            self._checkpointer = None
        if sqlite_path is not None:
            self.sqlite_path = sqlite_path

    def list_checkpoints(self, generation_id: str, limit: int = 20) -> list[dict]:
        config = {"configurable": {"thread_id": generation_id}}
        checkpoints = self.get_checkpointer().list(config, limit=limit)
        items: list[dict] = []
        for checkpoint_tuple in checkpoints:
            checkpoint = checkpoint_tuple.checkpoint
            items.append(
                {
                    "checkpoint_id": checkpoint_tuple.config["configurable"].get("checkpoint_id"),
                    "checkpoint_ns": checkpoint_tuple.config["configurable"].get("checkpoint_ns", ""),
                    "thread_id": checkpoint_tuple.config["configurable"].get("thread_id"),
                    "created_at": checkpoint.get("ts"),
                    "channel_keys": sorted(checkpoint.get("channel_values", {}).keys()),
                    "metadata": checkpoint_tuple.metadata,
                    "pending_write_count": len(checkpoint_tuple.pending_writes or []),
                }
            )
        return items

    def get_latest_result_snapshot(self, generation_id: str) -> ResultEnvelope | None:
        config = {"configurable": {"thread_id": generation_id}}
        checkpoint_tuple = self.get_checkpointer().get_tuple(config)
        if checkpoint_tuple is None:
            return None

        result_payload = checkpoint_tuple.checkpoint.get("channel_values", {}).get("result")
        if result_payload is None:
            return None
        return ResultEnvelope.model_validate(result_payload)

    def get_latest_checkpoint_state(self, generation_id: str) -> dict | None:
        from app.services.generation_pipeline.store import generation_pipeline_store

        config = {"configurable": {"thread_id": generation_id}}
        checkpoint_tuple = self.get_checkpointer().get_tuple(config)
        if checkpoint_tuple is None:
            return None

        record = generation_pipeline_store.get_record(generation_id)
        events = generation_pipeline_store.list_events(generation_id, limit=20)
        channel_values = checkpoint_tuple.checkpoint.get("channel_values", {})
        result_payload = channel_values.get("result")
        if isinstance(result_payload, ResultEnvelope):
            result_payload_dict = result_payload.model_dump(mode="json")
        else:
            result_payload_dict = result_payload or {}
        script_layer = result_payload_dict.get("result_package", {}).get("script_layer", {})
        segments = script_layer.get("segments", [])

        return {
            "checkpoint_id": checkpoint_tuple.config["configurable"].get("checkpoint_id"),
            "checkpoint_ns": checkpoint_tuple.config["configurable"].get("checkpoint_ns", ""),
            "thread_id": checkpoint_tuple.config["configurable"].get("thread_id"),
            "created_at": checkpoint_tuple.checkpoint.get("ts"),
            "channel_keys": sorted(channel_values.keys()),
            "metadata": checkpoint_tuple.metadata,
            "has_result": result_payload is not None,
            "result_title": result_payload_dict.get("result_package", {}).get("overview", {}).get("main_title"),
            "result_summary": result_payload_dict.get("result_package", {}).get("overview", {}).get(
                "one_sentence_summary"
            ),
            "script_segment_count": len(segments),
            "failure_attribution": self._build_failure_attribution(
                status=record.current_status,
                stage=str(record.current_stage),
                stage_message=record.stage_message,
                has_result_snapshot=result_payload is not None,
                events=events,
            ),
        }

    def delete_thread(self, generation_id: str) -> None:
        self.get_checkpointer().delete_thread(generation_id)

    def _build_failure_attribution(
        self,
        *,
        status: str | GenerationStatus,
        stage: str,
        stage_message: str,
        has_result_snapshot: bool,
        events: list[GenerationJobEventRecord],
    ) -> GenerationFailureAttribution:
        latest_error_event = next((event for event in reversed(events) if event.error_message), None)
        normalized_status = status.value if hasattr(status, "value") else str(status)

        if normalized_status == GenerationStatus.timeout.value:
            category = "timeout"
        elif normalized_status == GenerationStatus.failed.value:
            category = "execution_failed"
        else:
            category = "not_failed"

        if category == "not_failed":
            recovery_hint = "当前执行未进入失败态，可继续查看阶段推进和结果快照。"
        elif has_result_snapshot:
            recovery_hint = "当前失败态仍保留结果快照，可优先尝试从最新 checkpoint 恢复结果。"
        else:
            recovery_hint = "当前失败态未保留结果快照，应先查看最新错误事件、失败阶段和上游日志，再决定是否重试。"

        return GenerationFailureAttribution(
            category=category,
            stage=stage,
            stage_message=stage_message,
            latest_event_type=latest_error_event.event_type if latest_error_event is not None else None,
            latest_error_message=latest_error_event.error_message if latest_error_event is not None else None,
            recovery_hint=recovery_hint,
            can_restore_result_snapshot=has_result_snapshot,
        )


generation_checkpoint_service = GenerationCheckpointService()
