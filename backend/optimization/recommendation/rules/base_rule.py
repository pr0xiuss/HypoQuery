from __future__ import annotations

from abc import ABC, abstractmethod

from backend.optimization.recommendation.context import (
    RecommendationContext,
)
from backend.optimization.recommendation.helpers.finding_lookup import (
    FindingLookup,
)
from backend.optimization.recommendation.models.recommendation import (
    Recommendation,
)
from backend.optimization.recommendation.models.recommendation_collection import (
    RecommendationCollection,
)


class RecommendationRule(ABC):
    """
    Base contract for every recommendation rule.

    A rule examines the RecommendationContext and produces
    zero or more deterministic recommendations.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique rule name."""
        raise NotImplementedError

    @abstractmethod
    def recommend(
        self,
        context: RecommendationContext,
    ) -> RecommendationCollection:
        """
        Generates recommendations from the current analysis result.
        """
        raise NotImplementedError

    def findings(
        self,
        context: RecommendationContext,
    ) -> FindingLookup:
        """
        Returns a helper for querying analysis findings.
        """

        return FindingLookup(
            context,
        )

    def recommendations(self) -> RecommendationCollection:
        """
        Creates an empty recommendation collection.
        """

        return RecommendationCollection()

    def add(
        self,
        recommendations: RecommendationCollection,
        recommendation: Recommendation,
    ) -> None:
        """
        Adds a recommendation to the collection.
        """

        recommendations.add(
            recommendation,
        )