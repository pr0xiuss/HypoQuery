from __future__ import annotations

from backend.knowledge.projection.builders.base_relationship_builder import (
    RelationshipBuilder,
)
from backend.optimization.ranking.grouping.models.strategy import (
    Strategy,
)


class StrategyRelationshipBuilder(RelationshipBuilder):
    """
    Builds graph relationships originating from Strategies.

    Relationships are introduced in Module 2 once every
    projected node type exists.
    """

    def build(
        self,
        strategy: Strategy,
        **kwargs,
    ) -> list:

        return []