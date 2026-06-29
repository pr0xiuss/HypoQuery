from __future__ import annotations

from datetime import UTC, datetime

from backend.execution.contracts.enums import PipelineStatus
from backend.execution.contracts.execution import PipelineExecution
from backend.execution.contracts.result import PipelineResult
from backend.execution.contracts.exceptions import PipelineExecutionError
from .pipeline import Pipeline


class PipelineExecutor:
    """
    Executes a validated pipeline.
    """

    def execute(
        self,
        pipeline: Pipeline,
        execution: PipelineExecution,
    ) -> PipelineResult:

        started_at = datetime.now(UTC)

        execution.state.add_metric("started_at", started_at.isoformat())

        current = pipeline.definition.entry_node

        if pipeline.definition.entry_node is None:
            raise PipelineExecutionError(
                "Pipeline has no entry node."
            )

        while current is not None:

            node = pipeline.get_node(current)

            if node.can_execute(execution):

                try:

                    node.before_execute(execution)

                    result = node.execute(execution)

                    node.after_execute(execution, result)

                except Exception as exc:

                    execution.state.add_error(exc)

                    node.on_error(execution, exc)

                    return PipelineResult(
                        status=PipelineStatus.FAILED,
                        execution=execution,
                        started_at=started_at,
                        completed_at=datetime.now(UTC),
                        duration_ms=(
                            datetime.now(UTC) - started_at
                        ).total_seconds() * 1000,
                        summary=str(exc),
                    )

                finally:

                    node.cleanup(execution)

            current = pipeline.next_node(current)

        completed_at = datetime.now(UTC)

        duration_ms = (
            completed_at - started_at
        ).total_seconds() * 1000

        execution.state.add_metric("completed_at", completed_at.isoformat(),)

        execution.state.add_metric("duration_ms", duration_ms,)

        return PipelineResult(
            status=PipelineStatus.COMPLETED,
            execution=execution,
            started_at=started_at,
            completed_at=completed_at,
            duration_ms=duration_ms,
            summary="Pipeline executed successfully.",
        )