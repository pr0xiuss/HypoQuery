import time

from backend.execution.contracts.execution import PipelineExecution
from backend.execution.pipeline.base_node import PipelineNode
from backend.execution.runtime.runtime_context import RuntimeContext


class NodeRuntime:
    """
    Coordinates the execution of a single pipeline node.
    """

    def __init__(
        self,
        context: RuntimeContext,
    ) -> None:
        self._context = context

    def execute(
        self,
        node: PipelineNode,
        execution: PipelineExecution,
    ) -> None:
        node.before_execute(execution)

        started = self._context.clock.monotonic()

        started_event = self._context.event_factory.node_started(
            execution,
            node.name,
        )

        self._context.publisher.publish(started_event)

        try:
            result = node.execute(execution)

            node.after_execute(
                execution,
                result,
            )

            duration_ms = (
                self._context.clock.monotonic() - started
            ) * 1000

            execution.state.add_metric(
                f"{node.name}.duration_ms",
                round(duration_ms, 3),
            )

            completed_event = (
                self._context.event_factory.node_completed(
                    execution,
                    node.name,
                    duration_ms,
                )
            )

            self._context.publisher.publish(
                completed_event,
            )

        except Exception as exc:

            duration_ms = (
                self._context.clock.monotonic() - started
            ) * 1000

            execution.state.add_error(exc)

            node.on_error(
                execution,
                exc,
            )

            failed_event = (
                self._context.event_factory.node_failed(
                    execution,
                    node.name,
                    str(exc),
                    duration_ms,
                )
            )

            self._context.publisher.publish(
                failed_event,
            )

            raise

        finally:
            node.cleanup(execution)
            