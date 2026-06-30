from dataclasses import dataclass
from datetime import datetime

from .enums import PipelineStatus
from .execution import PipelineExecution


@dataclass(slots=True)
class PipelineResult:
    """
    Final result returned after pipeline execution.
    """

    status: PipelineStatus

    execution: PipelineExecution

    started_at: datetime

    completed_at: datetime

    duration_ms: float

    summary: str = ""