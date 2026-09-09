from backend.execution.contracts.execution import PipelineExecution
from backend.execution.runtime.runtime_context import RuntimeContext


class ExecutionRuntime:
    """
    Coordinates lifecycle transitions, event creation, and event publication.
    """

    def __init__(
        self,
        context: RuntimeContext,
    ) -> None:
        self._context = context

    def queue(
        self,
        execution: PipelineExecution,
    ) -> None:
        self._context.lifecycle.queue(execution)

        event = self._context.event_factory.queue_enqueued(
            execution,
        )

        self._context.publisher.publish(event)

    def assign(
        self,
        execution: PipelineExecution,
        worker_id: str,
    ) -> None:
        self._context.lifecycle.assign(execution)

        event = self._context.event_factory.worker_assigned(
            execution,
            worker_id,
        )

        self._context.publisher.publish(event)

    def start(
        self,
        execution: PipelineExecution,
    ) -> None:
        self._context.lifecycle.start(execution)

        execution.state.add_metric(
            "started_at",
            self._context.clock.now().isoformat(),
        )

        event = self._context.event_factory.pipeline_started(
            execution,
        )

        self._context.publisher.publish(event)

    def complete(
        self,
        execution: PipelineExecution,
        duration_ms: float,
    ) -> None:
        self._context.lifecycle.complete(execution)

        execution.state.add_metric(
            "completed_at",
            self._context.clock.now().isoformat(),
        )

        execution.state.add_metric(
            "duration_ms",
            duration_ms,
        )

        event = self._context.event_factory.pipeline_completed(
            execution,
            duration_ms,
        )

        self._context.publisher.publish(event)

    def fail(
        self,
        execution: PipelineExecution,
        error: str,
        error_type: str | None = None,
        duration_ms: float | None = None,
    ) -> None:
        self._context.lifecycle.fail(execution)

        event = self._context.event_factory.pipeline_failed(
            execution,
            error,
            error_type,
            duration_ms,
        )

        self._context.publisher.publish(event)

    def cancel(
        self,
        execution: PipelineExecution,
        reason: str | None = None,
    ) -> None:
        self._context.lifecycle.cancel(execution)

        event = self._context.event_factory.pipeline_cancelled(
            execution,
            reason,
        )

        self._context.publisher.publish(event)