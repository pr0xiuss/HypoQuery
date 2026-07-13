from __future__ import annotations

from uuid import uuid4

from backend.operations.contracts.snapshots import (
    MonitoringSnapshot,
)
from backend.operations.models.identifiers import (
    MonitoringId,
)
from backend.operations.monitoring.builders.monitoring_builder import (
    MonitoringBuilder,
)
from backend.operations.monitoring.engine import (
    MonitoringEngine,
)
from backend.operations.monitoring.models.baseline import (
    MonitoringBaseline,
)
from backend.operations.monitoring.models.finding import (
    MonitoringFinding,
)
from backend.operations.outcome.models.summary import (
    OutcomeSummary,
)


class MonitoringService:
    """
    Application service for
    Monitoring operations.
    """

    def __init__(
        self,
        engine: MonitoringEngine,
        builder: MonitoringBuilder,
    ) -> None:
        self._engine = engine
        self._builder = builder

    def create(
        self,
        *,
        outcome: OutcomeSummary,
        baseline: MonitoringBaseline,
        finding: MonitoringFinding,
    ) -> MonitoringSnapshot:

        monitoring = (
            self._builder
            .with_id(
                MonitoringId(
                    uuid4(),
                )
            )
            .with_outcome(
                outcome,
            )
            .with_baseline(
                baseline,
            )
            .with_finding(
                finding,
            )
            .build()
        )

        self._engine.create(
            monitoring,
        )

        return MonitoringSnapshot(
            monitoring_id=monitoring.id,
            health=monitoring.finding.health,
        )