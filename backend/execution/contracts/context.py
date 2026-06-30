from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True, slots=True)
class PipelineContext:
    """
    Immutable execution context.

    Describes WHAT is being processed.
    """

    database: str
    schema: str
    metadata: dict[str, Any] = field(default_factory=dict)