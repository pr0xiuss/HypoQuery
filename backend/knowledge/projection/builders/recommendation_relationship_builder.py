from __future__ import annotations

from backend.knowledge.projection.builders.base_relationship_builder import (
    RelationshipBuilder,
)
from backend.optimization.recommendation.models.recommendation import (
    Recommendation,
)


class RecommendationRelationshipBuilder(RelationshipBuilder):
    """
    Builds graph relationships originating from Recommendations.

    Phase 5 Module 1 intentionally produces no relationships.

    Recommendation relationships will be introduced after
    every primary node type has been projected.
    """

    def build(
        self,
        recommendation: Recommendation,
        **kwargs,
    ) -> list:

        return []