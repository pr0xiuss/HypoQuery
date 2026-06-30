from dataclasses import dataclass, field
from datetime import UTC, datetime
from backend.execution.contracts.execution import PipelineExecution
from backend.execution.contracts.job import PipelineJob


@dataclass(slots=True)
class QueueEntry:
    """
    Queue wrapper around a PipelineJob.

    Stores queue-specific metadata without modifying the PipelineJob itself.
    """

    execution: PipelineExecution

    submitted_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    attempts: int = 0