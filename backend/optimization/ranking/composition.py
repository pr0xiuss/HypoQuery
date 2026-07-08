from __future__ import annotations

from backend.optimization.ranking.engine import RankingEngine
from backend.optimization.ranking.policy import RankingPolicy
from backend.optimization.ranking.registry.scorer_registry import ScorerRegistry
from backend.optimization.ranking.scorers.confidence_scorer import ConfidenceScorer
from backend.optimization.ranking.scorers.impact_scorer import ImpactScorer
from backend.optimization.ranking.scorers.risk_scorer import RiskScorer
from backend.optimization.ranking.scorers.validation_scorer import ValidationScorer


def build_ranking_engine() -> RankingEngine:
    """
    Builds the ranking bounded context.
    """

    registry = ScorerRegistry()

    registry.register(
        ImpactScorer(),
    )

    registry.register(
        ValidationScorer(),
    )

    registry.register(
        ConfidenceScorer(),
    )

    registry.register(
        RiskScorer(),
    )

    return RankingEngine(
        registry,
        RankingPolicy(),
    )