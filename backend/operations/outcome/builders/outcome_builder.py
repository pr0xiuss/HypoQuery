from __future__ import annotations
from backend.operations.outcome.models.assessment import OutcomeAssessment
from backend.operations.models.identifiers import (
    OutcomeId,
)
from backend.operations.outcome.models.evidence import (
    OutcomeEvidence,
)
from backend.operations.outcome.models.metrics import (
    OutcomeMetrics,
)
from backend.operations.outcome.models.outcome import (
    Outcome,
)


class OutcomeBuilder:
    """
    Fluent builder for constructing
    Outcome aggregates.
    """

    def __init__(self) -> None:
        self._id: OutcomeId | None = None
        self._evidence: OutcomeEvidence | None = None
        self._metrics: OutcomeMetrics | None = None
        self._assessment: OutcomeAssessment | None = None

    def with_id(
        self,
        identifier: OutcomeId,
    ) -> "OutcomeBuilder":
        self._id = identifier
        return self

    def with_evidence(
        self,
        evidence: OutcomeEvidence,
    ) -> "OutcomeBuilder":
        self._evidence = evidence
        return self

    def with_metrics(
        self,
        metrics: OutcomeMetrics,
    ) -> "OutcomeBuilder":
        self._metrics = metrics
        return self

    def with_assessment(
        self,
        assessment: OutcomeAssessment,
    ) -> "OutcomeBuilder":
        self._assessment = assessment
        return self

    def build(self) -> Outcome:
        if self._id is None:
            raise ValueError(
                "Outcome identifier is required."
            )

        if self._evidence is None:
            raise ValueError(
                "Outcome evidence is required."
            )

        if self._metrics is None:
            raise ValueError(
                "Outcome metrics are required."
            )

        if self._assessment is None:
            raise ValueError(
                "Outcome assessment is required."
            )

        return Outcome(
            id=self._id,
            evidence=self._evidence,
            metrics=self._metrics,
            assessment=self._assessment,
        )