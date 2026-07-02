from __future__ import annotations

from datetime import UTC, datetime

from backend.execution.contracts.enums import PipelineStatus
from backend.execution.contracts.execution import PipelineExecution
from backend.execution.contracts.exceptions import PipelineExecutionError
from backend.execution.contracts.result import PipelineResult
from backend.execution.pipeline.pipeline import Pipeline
from backend.execution.runtime.execution_runtime import ExecutionRuntime
from backend.execution.runtime.node_runtime import NodeRuntime
from backend.shared.logger import get_logger


class PipelineExecutor:
    """
    Executes a validated pipeline.
    """

    def __init__(self, runtime: ExecutionRuntime, node_runtime: NodeRuntime,) -> None:
        
        self._runtime = runtime
        self._node_runtime = node_runtime
        self._logger = get_logger(self.__class__.__name__)

    def execute(self, pipeline: Pipeline, execution: PipelineExecution,) -> PipelineResult:

        started_at = datetime.now(UTC)

        self._runtime.queue(execution)

        self._runtime.assign(execution, worker_id="local-worker",)

        self._runtime.start(execution)

        current = pipeline.definition.entry_node

        if current is None:
            raise PipelineExecutionError("Pipeline has no entry node.")

        while current is not None:

            node = pipeline.get_node(current)

            if node.can_execute(execution):

                try:
                    self._node_runtime.execute(
                        node,
                        execution,
                    )

                except Exception as exc:

                    duration_ms = (
                        datetime.now(UTC) - started_at
                    ).total_seconds() * 1000

                    self._runtime.fail(
                        execution,
                        str(exc),
                        duration_ms,
                    )

                    return PipelineResult(
                        status=PipelineStatus.FAILED,
                        execution=execution,
                        started_at=started_at,
                        completed_at=datetime.now(UTC),
                        duration_ms=duration_ms,
                        summary=str(exc),
                    )

            current = pipeline.next_node(current)

        completed_at = datetime.now(UTC)

        duration_ms = (
            completed_at - started_at
        ).total_seconds() * 1000

        self._runtime.complete(
            execution,
            duration_ms,
        )

        return PipelineResult(
            status=PipelineStatus.COMPLETED,
            execution=execution,
            started_at=started_at,
            completed_at=completed_at,
            duration_ms=duration_ms,
            summary="Pipeline executed successfully.",
        )