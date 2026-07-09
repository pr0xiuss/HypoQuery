from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from backend.knowledge.retrieval.objectives.objective_type import (
    ObjectiveType,
)
from backend.knowledge.retrieval.objectives.retrieval_scope import (
    RetrievalScope,
)


@dataclass(frozen=True, slots=True)
class RetrievalObjective:
    """
    Immutable request describing the knowledge to retrieve.

    Retrieval objectives are independent of retrieval
    implementation.
    """

    type: ObjectiveType

    scope: RetrievalScope = RetrievalScope.LOCAL

    target: str | None = None

    parameters: dict[str, Any] = field(
        default_factory=dict,
    )