from dataclasses import dataclass, field
from typing import Any
from uuid import UUID


@dataclass(frozen=True, slots=True)
class PipelineContext:
    """
    Immutable execution context.

    Describes WHAT is being processed.
    """

    execution_id: UUID

    trace_id: UUID

    pipeline_name: str

    pipeline_version: str

    database: str

    schema: str

    metadata: dict[str, Any] = field(default_factory=dict)