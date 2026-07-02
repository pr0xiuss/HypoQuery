from backend.execution.contracts.execution import PipelineExecution
from backend.execution.contracts.lifecycle import Lifecycle
from backend.execution.lifecycle.enums import ExecutionStatus
from backend.execution.lifecycle.exceptions import InvalidStateTransitionError
from backend.execution.lifecycle.transitions import VALID_TRANSITIONS


class ExecutionLifecycle(Lifecycle):
    """
    Validates and applies execution lifecycle transitions.
    """

    def _transition(
        self,
        execution: PipelineExecution,
        target: ExecutionStatus,
    ) -> None:
        current = execution.state.status

        if target not in VALID_TRANSITIONS[current]:
            raise InvalidStateTransitionError(
                f"Invalid transition: {current.value} -> {target.value}"
            )

        execution.state.status = target

    def queue(
        self,
        execution: PipelineExecution,
    ) -> None:
        self._transition(
            execution,
            ExecutionStatus.QUEUED,
        )

    def assign(
        self,
        execution: PipelineExecution,
    ) -> None:
        self._transition(
            execution,
            ExecutionStatus.ASSIGNED,
        )

    def start(
        self,
        execution: PipelineExecution,
    ) -> None:
        self._transition(
            execution,
            ExecutionStatus.RUNNING,
        )

    def complete(
        self,
        execution: PipelineExecution,
    ) -> None:
        self._transition(
            execution,
            ExecutionStatus.COMPLETED,
        )

    def fail(
        self,
        execution: PipelineExecution,
    ) -> None:
        self._transition(
            execution,
            ExecutionStatus.FAILED,
        )

    def cancel(
        self,
        execution: PipelineExecution,
    ) -> None:
        self._transition(
            execution,
            ExecutionStatus.CANCELLED,
        )