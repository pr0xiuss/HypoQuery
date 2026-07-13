from __future__ import annotations

from uuid import uuid4

from backend.operations.contracts.snapshots import (
    OutcomeSnapshot,
)
from backend.operations.models.identifiers import (
    OutcomeId,
)
from backend.operations.outcome.builders.outcome_builder import (
    OutcomeBuilder,
)
from backend.operations.outcome.engine import (
    OutcomeEngine,
)
from backend.operations.outcome.models.assessment import (
    OutcomeAssessment,
)
from backend.operations.outcome.models.evidence import (
    OutcomeEvidence,
)
from backend.operations.outcome.models.metrics import (
    OutcomeMetrics,
)


class OutcomeService:
    """
    Application service for Outcome operations.
    """

    def __init__(
        self,
        engine: OutcomeEngine,
        builder: OutcomeBuilder,
    ) -> None:
        self._engine = engine
        self._builder = builder

    def create(
        self,
        *,
        evidence: OutcomeEvidence,
        metrics: OutcomeMetrics,
        assessment: OutcomeAssessment,
    ) -> OutcomeSnapshot:

        outcome = (
            self._builder
            .with_id(
                OutcomeId(
                    uuid4(),
                )
            )
            .with_evidence(
                evidence,
            )
            .with_metrics(
                metrics,
            )
            .with_assessment(
                assessment,
            )
            .build()
        )

        self._engine.create(
            outcome,
        )

        return OutcomeSnapshot(
            outcome_id=outcome.id,
            assessment=outcome.assessment,
        )