from __future__ import annotations

from backend.operations.models.identifiers import (
    MonitoringId,
)
from backend.operations.monitoring.models.baseline import (
    MonitoringBaseline,
)
from backend.operations.monitoring.models.finding import (
    MonitoringFinding,
)
from backend.operations.monitoring.models.monitoring import (
    Monitoring,
)
from backend.operations.outcome.models.summary import (
    OutcomeSummary,
)


class MonitoringBuilder:
    """
    Fluent builder for constructing
    Monitoring aggregates.
    """

    def __init__(self) -> None:
        self._id: MonitoringId | None = None
        self._outcome: OutcomeSummary | None = None
        self._baseline: MonitoringBaseline | None = None
        self._finding: MonitoringFinding | None = None

    def with_id(
        self,
        identifier: MonitoringId,
    ) -> "MonitoringBuilder":
        self._id = identifier
        return self

    def with_outcome(
        self,
        outcome: OutcomeSummary,
    ) -> "MonitoringBuilder":
        self._outcome = outcome
        return self

    def with_baseline(
        self,
        baseline: MonitoringBaseline,
    ) -> "MonitoringBuilder":
        self._baseline = baseline
        return self

    def with_finding(
        self,
        finding: MonitoringFinding,
    ) -> "MonitoringBuilder":
        self._finding = finding
        return self

    def build(self) -> Monitoring:
        if self._id is None:
            raise ValueError(
                "Monitoring identifier is required."
            )

        if self._outcome is None:
            raise ValueError(
                "Outcome summary is required."
            )

        if self._baseline is None:
            raise ValueError(
                "Monitoring baseline is required."
            )

        if self._finding is None:
            raise ValueError(
                "Monitoring finding is required."
            )

        return Monitoring(
            id=self._id,
            outcome=self._outcome,
            baseline=self._baseline,
            finding=self._finding,
        )