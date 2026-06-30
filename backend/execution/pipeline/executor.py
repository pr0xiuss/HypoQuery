from __future__ import annotations
import time
from datetime import UTC, datetime
from backend.shared.logger import get_logger
from backend.execution.contracts.enums import PipelineStatus
from backend.execution.contracts.execution import PipelineExecution
from backend.execution.contracts.result import PipelineResult
from backend.execution.contracts.exceptions import PipelineExecutionError
from .pipeline import Pipeline


class PipelineExecutor:
    """
    Executes a validated pipeline.
    """
    def __init__(self) -> None:
        self._logger = get_logger(self.__class__.__name__)

    def execute(self, pipeline: Pipeline, execution: PipelineExecution,) -> PipelineResult:

        started_at = datetime.now(UTC)

        self._logger.info(
            "Pipeline Started | "
            f"pipeline={pipeline.definition.pipeline_id} | "
            f"source={execution.job.source}"
        )

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

                    node_started = time.perf_counter()

                    self._logger.info(
                        f"Node Started | node={current}"
                    )

                    result = node.execute(execution)

                    node.after_execute(execution, result)

                    node_duration = (
                        time.perf_counter() - node_started
                    ) * 1000

                    execution.state.add_metric(
                        f"{current}.duration_ms",
                        round(node_duration, 3),
                    )

                    self._logger.info(
                        "Node Completed | "
                        f"node={current} | "
                        f"duration_ms={node_duration:.3f}"
                    )

                except Exception as exc:

                    self._logger.exception(
                        f"Node Failed | node={current}"
                    )

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

        self._logger.info(
            "Pipeline Completed | "
            f"pipeline={pipeline.definition.pipeline_id} | "
            f"status=COMPLETED | "
            f"duration_ms={duration_ms:.3f}"
        )

        return PipelineResult(
            status=PipelineStatus.COMPLETED,
            execution=execution,
            started_at=started_at,
            completed_at=completed_at,
            duration_ms=duration_ms,    
            summary="Pipeline executed successfully.",
        )