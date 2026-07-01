from dataclasses import dataclass, field

from backend.execution.contracts.context import PipelineContext
from backend.execution.contracts.job import PipelineJob
from backend.execution.contracts.state import PipelineState


@dataclass(slots=True)
class PipelineExecution:
    """
    Represents a single execution of a pipeline.

    Combines immutable identity/context with mutable execution state.
    """

    job: PipelineJob
    context: PipelineContext

    state: PipelineState = field(default_factory=PipelineState)