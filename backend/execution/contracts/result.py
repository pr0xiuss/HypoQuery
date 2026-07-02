from dataclasses import dataclass
from datetime import datetime

from backend.execution.contracts.enums import PipelineStatus
from backend.execution.contracts.execution import PipelineExecution


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