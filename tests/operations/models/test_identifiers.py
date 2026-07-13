from dataclasses import FrozenInstanceError
from uuid import uuid4

import pytest

from backend.operations.models.identifiers import (
    MonitoringFindingId,
    OperationalAssessmentId,
    OptimizationCaseId,
    VerificationId,
)


def test_optimization_case_identifier_is_immutable() -> None:
    identifier = OptimizationCaseId(uuid4())

    with pytest.raises(FrozenInstanceError):
        identifier.value = uuid4()


def test_verification_identifier_equality() -> None:
    value = uuid4()

    left = VerificationId(value)
    right = VerificationId(value)

    assert left == right


def test_operational_assessment_identifier_holds_uuid() -> None:
    value = uuid4()

    identifier = OperationalAssessmentId(value)

    assert identifier.value == value


def test_monitoring_finding_identifier_holds_uuid() -> None:
    value = uuid4()

    identifier = MonitoringFindingId(value)

    assert identifier.value == value