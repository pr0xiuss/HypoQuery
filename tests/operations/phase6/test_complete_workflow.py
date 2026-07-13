from uuid import uuid4

from backend.operations.models.enums import (
    CasePriority,
    OptimizationHealthStatus,
    PolicyDecisionType,
)
from backend.operations.models.identifiers import (
    VerificationId,
)

from backend.operations.monitoring.models.baseline import (
    MonitoringBaseline,
)

from backend.operations.monitoring.models.finding import (
    MonitoringFinding,
)

from backend.operations.outcome.models.evidence import (
    OutcomeEvidence,
)

from backend.operations.outcome.models.metrics import (
    OutcomeMetrics,
)

from backend.operations.verification.models.summary import (
    VerificationSummary,
)
from backend.operations.models.references import (
    RecommendationReference,
)
from backend.operations.monitoring.models.health import (
    OptimizationHealth,
)
from backend.operations.monitoring.models.summary import (
    MonitoringSummary,
)
from backend.operations.outcome.models.assessment import (
    OutcomeAssessment,
)
from backend.operations.outcome.models.summary import (
    OutcomeSummary,
)
from backend.operations.policy.models.decision import (
    PolicyDecision,
)
from backend.operations.policy.models.rule import (
    PolicyRule,
)
from backend.operations.integration.composition import (
    OperationsIntegrationComposition,
)
from backend.optimization.recommendation.models.recommendation_key import (
    RecommendationKey,
)
from backend.operations.cases.models.recommendation_reference_collection import (
    RecommendationReferenceCollection,
)
from backend.operations.cases.models.metadata import (
    CaseMetadata,
)
from backend.optimization.recommendation.models.recommendation_key import (
    RecommendationKey,
)
from backend.operations.models.references import (
    RecommendationReference,
)
from backend.operations.models.enums import (
    CaseIntent,
)

def test_complete_operations_workflow() -> None:
    context = (
        OperationsIntegrationComposition()
        .compose()
    )

    recommendation = RecommendationReference(
        key=RecommendationKey(
            category="INDEX",
            target="users.email",
            action="CREATE",
        ),
        recommendation_code="IDX_USERS_EMAIL",
        recommendation_version=1,
    )

    case = context.cases.service.create(
        recommendations=RecommendationReferenceCollection(
            recommendations=[
                recommendation,
            ],
        ),
        metadata=CaseMetadata(
            intent=CaseIntent.PERFORMANCE,
            labels=[
                "phase6",
                "workflow",
            ],
        ),
        priority=CasePriority.HIGH,
    )

    verification_summary = VerificationSummary(
        id=VerificationId(uuid4()),
        verified=True,
    )

    outcome = context.outcome.service.create(
        evidence=OutcomeEvidence(
            verification=verification_summary,
            summary="Verification completed successfully.",
        ),
        metrics=OutcomeMetrics(
            performance_improvement=12.5,
            storage_overhead=0.5,
            maintenance_cost=0.2,
        ),
        assessment=OutcomeAssessment(
            category="SUCCESSFUL",
            confidence=0.95,
            summary="Optimization successful.",
        ),
    )

    monitoring = context.monitoring.service.create(
        outcome=OutcomeSummary(
            id=outcome.outcome_id,
            assessment=outcome.assessment,
        ),
        baseline=MonitoringBaseline(
            execution_time=100.0,
            shared_buffers=250.0,
            planning_time=2.5,
        ),
        finding=MonitoringFinding(
            health=OptimizationHealth(
                status=OptimizationHealthStatus.HEALTHY,
                confidence=0.98,
                summary="Healthy.",
            ),
            regression_detected=False,
            confidence=0.99,
            summary="No regression detected.",
        ),
    )

    policy = context.policy.service.create(
        monitoring=MonitoringSummary(
            id=monitoring.monitoring_id,
            health=monitoring.health,
        ),
        rule=PolicyRule(
            name="Default Policy",
            threshold=5.0,
            description="Default rule.",
        ),
        decision=PolicyDecision(
            decision=PolicyDecisionType.NO_ACTION,
            confidence=0.99,
            summary="Everything looks good.",
        ),
    )

    assert case is not None
    assert outcome is not None
    assert monitoring is not None
    assert policy is not None