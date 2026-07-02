from backend.execution.lifecycle.enums import ExecutionStatus


VALID_TRANSITIONS: dict[ExecutionStatus, set[ExecutionStatus]] = {
    ExecutionStatus.CREATED: {
        ExecutionStatus.QUEUED,
        ExecutionStatus.CANCELLED,
    },

    ExecutionStatus.QUEUED: {
        ExecutionStatus.ASSIGNED,
        ExecutionStatus.CANCELLED,
    },

    ExecutionStatus.ASSIGNED: {
        ExecutionStatus.RUNNING,
        ExecutionStatus.FAILED,
        ExecutionStatus.CANCELLED,
    },

    ExecutionStatus.RUNNING: {
        ExecutionStatus.COMPLETED,
        ExecutionStatus.FAILED,
        ExecutionStatus.CANCELLED,
    },

    ExecutionStatus.COMPLETED: set(),

    ExecutionStatus.FAILED: set(),

    ExecutionStatus.CANCELLED: set(),
}