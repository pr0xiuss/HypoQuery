from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from backend.knowledge.models.context_priority import (
    ContextPriority,
)


@dataclass(slots=True)
class ContextSection:
    """
    Represents one logical section of an optimization context.

    Each builder contributes one or more sections that are
    later assembled into a complete OptimizationContext.
    """

    title: str

    priority: ContextPriority

    attributes: dict[
        str,
        Any,
    ] = field(
        default_factory=dict,
    )