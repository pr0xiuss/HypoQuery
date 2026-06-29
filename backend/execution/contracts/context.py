from dataclasses import dataclass, field
from typing import Any
from .fingerprint import QueryFingerprint


@dataclass(frozen=True, slots=True)
class PipelineContext:
    """
    Immutable execution context.

    Describes WHAT is being processed.
    """

    fingerprint: QueryFingerprint
    database: str
    schema: str
    metadata: dict[str, Any] = field(default_factory=dict)