from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import uuid4, UUID

from .enums import JobPriority


@dataclass(slots=True)
class PipelineJob:
    """
    Represents a unit of work flowing through the execution infrastructure.
    """

    source: str
    pipeline_version: str
    priority: JobPriority = JobPriority.NORMAL
    job_id: UUID = field(default_factory=uuid4)
    trace_id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))