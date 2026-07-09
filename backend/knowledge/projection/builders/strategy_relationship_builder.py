from __future__ import annotations

from backend.knowledge.models.enums import (
    KnowledgeRelationshipType,
)
from backend.knowledge.models.knowledge_graph import (
    KnowledgeGraph,
)
from backend.knowledge.models.knowledge_relationship import (
    KnowledgeRelationship,
)
from backend.knowledge.models.node_key import (
    NodeKey,
)
from backend.knowledge.models.relationship_key import (
    RelationshipKey,
)
from backend.optimization.ranking.grouping.models.strategy import (
    Strategy,
)


class StrategyRelationshipBuilder:
    """
    Builds semantic relationships originating from Strategies.
    """

    def build(
        self,
        strategy: Strategy,
        graph: KnowledgeGraph,
    ) -> list[KnowledgeRelationship]:

        relationships: list[
            KnowledgeRelationship
        ] = []

        rankings = (
            strategy.representative,
            *strategy.alternatives,
        )

        strategy_key = NodeKey(
            f"strategy:{strategy.strategy_type.value}"
        )

        for ranking in rankings:

            recommendation = ranking.recommendation

            recommendation_key = NodeKey(
                f"recommendation:{recommendation.code}"
            )

            if not graph.contains_node(
                recommendation_key,
            ):
                continue

            relationships.append(
                KnowledgeRelationship(
                    key=RelationshipKey(
                        f"{strategy.strategy_type.value}->{recommendation.code}"
                    ),
                    type=KnowledgeRelationshipType.CONTAINS,
                    source=strategy_key,
                    target=recommendation_key,
                )
            )

        return relationships