from __future__ import annotations

from backend.optimization.analysis.models.finding import Finding
from backend.optimization.recommendation.context import (
    RecommendationContext,
)


class FindingLookup:
    """
    Helper for querying findings produced by Analysis.

    Recommendation rules should use this helper instead of
    manually iterating over FindingCollection.
    """

    def __init__(
        self,
        context: RecommendationContext,
    ) -> None:

        self._findings = list(
            context.analysis_result.findings,
        )

    def has(
        self,
        code: str,
    ) -> bool:

        return self.get(code) is not None

    def has_any(
        self,
        *codes: str,
    ) -> bool:

        return any(
            self.has(code)
            for code in codes
        )

    def has_all(
        self,
        *codes: str,
    ) -> bool:

        return all(
            self.has(code)
            for code in codes
        )

    def get(
        self,
        code: str,
    ) -> Finding | None:

        for finding in self._findings:

            if finding.code == code:
                return finding

        return None

    def find_all(
        self,
        code: str,
    ) -> list[Finding]:

        return [
            finding
            for finding in self._findings
            if finding.code == code
        ]
    
    def count(
        self,
        code: str,
    ) -> int:
        """
        Returns the number of findings matching the given code.
        """

        return len(
            self.find_all(
                code,
            )
        )