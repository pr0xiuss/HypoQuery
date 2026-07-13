from uuid import uuid4

from backend.operations.models.identifiers import (
    VerificationId,
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
from backend.operations.outcome.repositories.memory_repository import (
    MemoryOutcomeRepository,
)
from backend.operations.outcome.service import (
    OutcomeService,
)
from backend.operations.verification.models.summary import (
    VerificationSummary,
)


def test_service_creates_outcome_snapshot() -> None:
    repository = MemoryOutcomeRepository()

    service = OutcomeService(
        engine=OutcomeEngine(
            repository,
        ),
        builder=OutcomeBuilder(),
    )

    snapshot = service.create(
        evidence=OutcomeEvidence(
            verification=VerificationSummary(
                id=VerificationId(uuid4()),
                verified=True,
            ),
            summary="Verification completed.",
        ),
        metrics=OutcomeMetrics(
            performance_improvement=65.0,
            storage_overhead=3.0,
            maintenance_cost=1.0,
        ),
        assessment=OutcomeAssessment(
            category="SUCCESSFUL",
            confidence=0.95,
            summary="Optimization succeeded.",
        ),
    )

    assert snapshot.assessment.category == "SUCCESSFUL"