from dataclasses import dataclass
from typing import Optional


from backend.execution.contracts.events.base import PipelineEvent


@dataclass(frozen=True, slots=True)
class PipelineStartedEvent(PipelineEvent):
    """
    Published when pipeline execution begins.
    """


@dataclass(frozen=True, slots=True)
class PipelineCompletedEvent(PipelineEvent):
    """
    Published when pipeline execution completes successfully.
    """

    duration_ms: float


@dataclass(frozen=True, slots=True)
class PipelineFailedEvent(PipelineEvent):
    """
    Published when pipeline execution fails.
    """

    error: str
    duration_ms: Optional[float] = None


@dataclass(frozen=True, slots=True)
class PipelineCancelledEvent(PipelineEvent):
    """
    Published when pipeline execution is cancelled.
    """

    reason: str | None = None