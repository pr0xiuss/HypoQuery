from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class RecommendationMetadata:
    """
    Additional structured information associated with a recommendation.

    Stores deterministic provenance required by downstream
    bounded contexts.
    """

    originating_findings: list[str] = field(
        default_factory=list,
    )

    attributes: dict[str, object] = field(
        default_factory=dict,
    )