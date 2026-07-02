from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from backend.execution.lifecycle.enums import ExecutionStatus


@dataclass(slots=True)
class ExecutionProjection:
    """
    Current read model for a pipeline execution.

    Derived entirely from execution events.
    """

    execution_id: UUID

    trace_id: UUID

    status: ExecutionStatus = ExecutionStatus.CREATED

    started_at: datetime | None = None

    completed_at: datetime | None = None

    duration_ms: float | None = None

    nodes_started: int = 0

    nodes_completed: int = 0

    nodes_failed: int = 0

    queue_time: datetime | None = None

    assigned_at: datetime | None = None

    assigned_worker: str | None = None