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
from backend.optimization.recommendation.models.recommendation import (
    Recommendation,
)


class RecommendationRelationshipBuilder:
    """
    Builds semantic relationships originating from Recommendations.
    """

    def build(
        self,
        recommendation: Recommendation,
        graph: KnowledgeGraph,
    ) -> list[KnowledgeRelationship]:

        relationships: list[
            KnowledgeRelationship
        ] = []

        for finding_code in (
            recommendation.metadata.originating_findings
        ):

            finding_key = NodeKey(
                f"finding:{finding_code}"
            )

            if graph.contains_node(
                finding_key,
            ):

                relationships.append(
                    KnowledgeRelationship(
                        key=RelationshipKey(
                            f"{finding_code}->{recommendation.code}"
                        ),
                        type=KnowledgeRelationshipType.LEADS_TO,
                        source=finding_key,
                        target=NodeKey(
                            f"recommendation:{recommendation.code}"
                        ),
                    )
                )

        validation_key = NodeKey(
            f"validation:{recommendation.code}"
        )

        if graph.contains_node(
            validation_key,
        ):

            relationships.append(
                KnowledgeRelationship(
                    key=RelationshipKey(
                        f"{recommendation.code}->validation"
                    ),
                    type=KnowledgeRelationshipType.VALIDATED_BY,
                    source=NodeKey(
                        f"recommendation:{recommendation.code}"
                    ),
                    target=validation_key,
                )
            )

        return relationships