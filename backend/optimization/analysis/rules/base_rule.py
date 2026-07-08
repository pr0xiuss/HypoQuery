from __future__ import annotations

from abc import ABC, abstractmethod

from backend.optimization.analysis.context import AnalysisContext
from backend.optimization.analysis.models.finding_collection import FindingCollection


class AnalysisRule(ABC):
    """
    Base contract for all analysis rules.

    A rule performs one deterministic observation over the
    supplied AnalysisContext and produces zero or more Findings.
    Rules must be stateless and independent.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique rule name."""
        raise NotImplementedError

    @abstractmethod
    def analyze(self, context: AnalysisContext) -> FindingCollection:
        """
        Analyze the supplied context.

        Returns:
            A list of findings. An empty list indicates that the
            rule did not detect anything noteworthy.
        """
        raise NotImplementedError