from uuid import uuid4

import pytest

from backend.operations.models.enums import (
    OptimizationHealthStatus,
)
from backend.operations.models.identifiers import (
    MonitoringId,
    OutcomeId,
)
from backend.operations.monitoring.builders.monitoring_builder import (
    MonitoringBuilder,
)
from backend.operations.monitoring.models.baseline import (
    MonitoringBaseline,
)
from backend.operations.monitoring.models.finding import (
    MonitoringFinding,
)
from backend.operations.monitoring.models.health import (
    OptimizationHealth,
)
from backend.operations.outcome.models.assessment import (
    OutcomeAssessment,
)
from backend.operations.outcome.models.summary import (
    OutcomeSummary,
)


def build_outcome() -> OutcomeSummary:
    return OutcomeSummary(
        id=OutcomeId(uuid4()),
        assessment=OutcomeAssessment(
            category="SUCCESSFUL",
            confidence=0.95,
            summary="Optimization successful.",
        ),
    )


def test_builder_builds_monitoring() -> None:
    monitoring = (
        MonitoringBuilder()
        .with_id(
            MonitoringId(uuid4()),
        )
        .with_outcome(
            build_outcome(),
        )
        .with_baseline(
            MonitoringBaseline(
                execution_time=100.0,
                shared_buffers=50.0,
                planning_time=4.0,
            ),
        )
        .with_finding(
            MonitoringFinding(
                health=OptimizationHealth(
                    status=OptimizationHealthStatus.HEALTHY,
                    confidence=0.96,
                    summary="Healthy.",
                ),
                regression_detected=False,
                confidence=0.97,
                summary="No regression.",
            ),
        )
        .build()
    )

    assert (
        monitoring.finding.health.status
        == OptimizationHealthStatus.HEALTHY
    )


def test_builder_requires_identifier() -> None:
    builder = (
        MonitoringBuilder()
        .with_outcome(
            build_outcome(),
        )
        .with_baseline(
            MonitoringBaseline(
                execution_time=100.0,
                shared_buffers=50.0,
                planning_time=4.0,
            ),
        )
        .with_finding(
            MonitoringFinding(
                health=OptimizationHealth(
                    status=OptimizationHealthStatus.HEALTHY,
                    confidence=0.96,
                    summary="Healthy.",
                ),
                regression_detected=False,
                confidence=0.97,
                summary="No regression.",
            ),
        )
    )

    with pytest.raises(
        ValueError,
    ):
        builder.build()