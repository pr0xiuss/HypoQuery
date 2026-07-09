from __future__ import annotations

from backend.knowledge.models.node_key import NodeKey
from backend.optimization.analysis.models.finding import Finding
from backend.optimization.recommendation.models.recommendation import (
    Recommendation,
)
from backend.optimization.ranking.grouping.models.strategy import (
    Strategy,
)
from backend.optimization.validation.models.validation import (
    Validation,
)


class NodeIdentity:
    """
    Generates deterministic identities for KnowledgeNodes.

    All KnowledgeNode identities are centralized here to ensure
    consistency across projection, replay, and graph rebuilds.
    """

    @staticmethod
    def for_finding(
        finding: Finding,
    ) -> NodeKey:
        return NodeKey(
            value=f"finding:{finding.category.value}:{finding.code}",
        )

    @staticmethod
    def for_recommendation(
        recommendation: Recommendation,
    ) -> NodeKey:
        return NodeKey(
            value=(
                f"recommendation:"
                f"{recommendation.category.value}:"
                f"{recommendation.code}"
            ),
        )

    @staticmethod
    def for_validation(
        validation: Validation,
    ) -> NodeKey:
        return NodeKey(
            value=(
                f"validation:"
                f"{validation.recommendation.key.value}:"
                f"{validation.validation_type.value}"
            ),
        )

    @staticmethod
    def for_strategy(
        strategy: Strategy,
    ) -> NodeKey:
        return NodeKey(
            value=(
                f"strategy:"
                f"{strategy.strategy_type.value}:"
                f"{strategy.representative.recommendation.key.value}"
            ),
        )