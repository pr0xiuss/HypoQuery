from datetime import UTC, datetime
from uuid import uuid4

from backend.execution.contracts.events.enums import EventVersion
from backend.execution.events.metadata import EventMetadata
from backend.operations.events.base_event import (
    CaseEvent,
    MonitoringEvent,
    OperationsEvent,
    OperationalAssessmentEvent,
    VerificationEvent,
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


def test_operations_event_creation() -> None:
    metadata = build_metadata()

    event = OperationsEvent(metadata=metadata)

    assert event.metadata == metadata


def test_case_event_inherits_operations_event() -> None:
    event = CaseEvent(metadata=build_metadata())

    assert isinstance(event, OperationsEvent)


def test_verification_event_inherits_operations_event() -> None:
    event = VerificationEvent(metadata=build_metadata())

    assert isinstance(event, OperationsEvent)


def test_operational_assessment_event_inherits_operations_event() -> None:
    event = OperationalAssessmentEvent(
        metadata=build_metadata(),
    )

    assert isinstance(event, OperationsEvent)


def test_monitoring_event_inherits_operations_event() -> None:
    event = MonitoringEvent(metadata=build_metadata())

    assert isinstance(event, OperationsEvent)