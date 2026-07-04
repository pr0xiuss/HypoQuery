from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterator

from backend.optimization.analysis.models.finding import Finding


@dataclass(slots=True)
class FindingCollection:
    """
    Represents all findings produced during a single analysis execution.

    This is intentionally a lightweight collection and not
    a rich aggregate. The aggregate root exposed outside the
    Analysis bounded context is AnalysisResult.
    """

    findings: list[Finding] = field(default_factory=list)

    def add(self, finding: Finding) -> None:
        self.findings.append(finding)

    def extend(self, findings: "FindingCollection",) -> None:
        for finding in findings:
            self.add(finding)

    def __iter__(self) -> Iterator[Finding]:
        return iter(self.findings)

    def __len__(self) -> int:
        return len(self.findings)

    def is_empty(self) -> bool:
        return len(self.findings) == 0