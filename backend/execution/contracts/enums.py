from enum import Enum


class JobPriority(Enum):
    """Priority assigned to a pipeline job."""

    CRITICAL = "critical"
    HIGH = "high"
    NORMAL = "normal"
    LOW = "low"
    BACKGROUND = "background"


class PipelineStatus(Enum):
    """Represents the lifecycle state of a pipeline execution."""

    CREATED = "created"
    QUEUED = "queued"
    RUNNING = "running"
    RETRYING = "retrying"
    FAILED = "failed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class NodeStatus(Enum):
    """Outcome of an individual pipeline node."""

    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"
    RETRY = "retry"
    STOP = "stop"