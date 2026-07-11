from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from backend.knowledge.models.explanation_priority import (
    ExplanationPriority,
)


@dataclass(slots=True)
class ExplanationSection:
    """
    Represents one logical explanation produced from an
    OptimizationContext.

    Sections remain deterministic and renderer-agnostic.
    """

    title: str

    priority: ExplanationPriority

    content: dict[
        str,
        Any,
    ] = field(
        default_factory=dict,
    )