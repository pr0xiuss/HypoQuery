from __future__ import annotations

from dataclasses import dataclass

from backend.knowledge.models.explanation import (
    Explanation,
)
from backend.knowledge.models.explanation_metadata import (
    ExplanationMetadata,
)


@dataclass(frozen=True, slots=True)
class ExplanationSnapshot:
    """
    Immutable snapshot of a generated Explanation.

    ExplanationSnapshots are the canonical output of
    the Explanation Engine.
    """

    metadata: ExplanationMetadata

    explanation: Explanation