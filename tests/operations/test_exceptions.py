from backend.operations.exceptions.exceptions import (
    CaseError,
    MonitoringError,
    OperationalAssessmentError,
    OperationsError,
    PolicyEvaluationError,
    VerificationError,
)


def test_case_error_inherits_operations_error() -> None:
    assert issubclass(
        CaseError,
        OperationsError,
    )


def test_verification_error_inherits_operations_error() -> None:
    assert issubclass(
        VerificationError,
        OperationsError,
    )


def test_operational_assessment_error_inherits_operations_error() -> None:
    assert issubclass(
        OperationalAssessmentError,
        OperationsError,
    )


def test_monitoring_error_inherits_operations_error() -> None:
    assert issubclass(
        MonitoringError,
        OperationsError,
    )


def test_policy_evaluation_error_inherits_operations_error() -> None:
    assert issubclass(
        PolicyEvaluationError,
        OperationsError,
    )