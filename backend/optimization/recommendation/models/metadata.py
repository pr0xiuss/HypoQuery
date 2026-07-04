from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class RecommendationMetadata:
    """
    Additional structured information associated with a recommendation.

    This metadata is intended for downstream consumers such as
    validators, reporters, or AI explanations.
    """

    attributes: dict[str, Any] = field(default_factory=dict)