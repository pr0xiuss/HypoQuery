from dataclasses import dataclass, field

from .context import PipelineContext
from .job import PipelineJob
from .state import PipelineState


@dataclass(slots=True)
class PipelineExecution:
    """
    Represents a single execution of a pipeline.

    Combines immutable identity/context with mutable execution state.
    """

    job: PipelineJob
    context: PipelineContext

    state: PipelineState = field(default_factory=PipelineState)