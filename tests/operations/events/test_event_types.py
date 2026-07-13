from datetime import UTC, datetime
from uuid import uuid4

from backend.execution.contracts.events.enums import EventVersion
from backend.execution.events.metadata import EventMetadata
from backend.operations.events.base_event import (
    CaseEvent,
    MonitoringEvent,
    OperationalAssessmentEvent,
    VerificationEvent,
)
from backend.operations.events.event_types import (
    CaseArchivedEvent,
    CaseCreatedEvent,
    OperationalAssessmentCompletedEvent,
    OptimizationVerifiedEvent,
    RegressionDetectedEvent,
)


def build_metadata() -> EventMetadata:
    return EventMetadata(
        event_id=uuid4(),
        execution_id=uuid4(),
        trace_id=uuid4(),
        sequence_number=1,
        timestamp=datetime.now(UTC),
        event_version=EventVersion.V1,
    )


def test_case_created_event_type() -> None:
    event = CaseCreatedEvent(
        metadata=build_metadata(),
    )

    assert isinstance(event, CaseEvent)


def test_case_archived_event_type() -> None:
    event = CaseArchivedEvent(
        metadata=build_metadata(),
    )

    assert isinstance(event, CaseEvent)


def test_optimization_verified_event_type() -> None:
    event = OptimizationVerifiedEvent(
        metadata=build_metadata(),
    )

    assert isinstance(event, VerificationEvent)


def test_operational_assessment_completed_event_type() -> None:
    event = OperationalAssessmentCompletedEvent(
        metadata=build_metadata(),
    )

    assert isinstance(
        event,
        OperationalAssessmentEvent,
    )


def test_regression_detected_event_type() -> None:
    event = RegressionDetectedEvent(
        metadata=build_metadata(),
    )

    assert isinstance(event, MonitoringEvent)