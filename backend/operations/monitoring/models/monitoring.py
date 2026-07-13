from __future__ import annotations

from dataclasses import dataclass

from backend.operations.models.identifiers import (
    MonitoringId,
)
from backend.operations.outcome.models.summary import (
    OutcomeSummary,
)
from backend.operations.monitoring.models.baseline import (
    MonitoringBaseline,
)
from backend.operations.monitoring.models.finding import (
    MonitoringFinding,
)


@dataclass(
    slots=True,
)
class Monitoring:
    """
    Aggregate representing continuous
    monitoring of a completed optimization.
    """

    id: MonitoringId

    outcome: OutcomeSummary

    baseline: MonitoringBaseline

    finding: MonitoringFinding