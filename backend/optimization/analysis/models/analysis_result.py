from __future__ import annotations

from dataclasses import dataclass, field

from backend.optimization.analysis.models.finding_collection import (
    FindingCollection,
)


@dataclass(slots=True)
class AnalysisResult:
    """
    Published contract of the Analysis bounded context.

    Represents the deterministic observations produced
    during one analysis execution.
    """

    findings: FindingCollection = field(
        default_factory=FindingCollection,
    )

    metadata: dict[str, object] = field(
        default_factory=dict,
    )

    @property
    def total_findings(self) -> int:
        return len(self.findings)