from enum import Enum


class ExecutionStatus(str, Enum):
    """
    Runtime lifecycle state of a pipeline execution.
    """

    CREATED = "created"

    QUEUED = "queued"

    ASSIGNED = "assigned"

    RUNNING = "running"

    COMPLETED = "completed"

    FAILED = "failed"

    CANCELLED = "cancelled"