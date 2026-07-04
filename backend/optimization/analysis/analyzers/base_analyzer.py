from __future__ import annotations

from abc import ABC, abstractmethod

from backend.optimization.analysis.context import AnalysisContext
from backend.optimization.analysis.models.finding_collection import FindingCollection


class Analyzer(ABC):
    """
    Base contract for every Analysis domain.

    An analyzer orchestrates a family of Analysis Rules
    (Execution, Health, Configuration, Workload, etc.)
    and produces deterministic Findings.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique analyzer name."""
        raise NotImplementedError

    @abstractmethod
    def analyze(self, context: AnalysisContext) -> FindingCollection:
        """
        Execute analysis for this domain.

        Returns:
            Findings produced by this analyzer.
        """
        raise NotImplementedError