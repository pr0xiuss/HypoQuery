from backend.optimization.reporting.models.validation_report import (
    ValidationReport,
)
from backend.optimization.validation.models.validation_status import (
    ValidationStatus,
)
from backend.optimization.validation.models.validation_type import (
    ValidationType,
)


def test_validation_report():

    report = ValidationReport(
        status=ValidationStatus.VALIDATED,
        validation_type=ValidationType.HYPOTHETICAL_INDEX,
        improvement_percent=81.4,
        cost_before=120.0,
        cost_after=22.3,
        plan_changed=True,
    )

    assert (
        report.status
        == ValidationStatus.VALIDATED
    )

    assert (
        report.validation_type
        == ValidationType.HYPOTHETICAL_INDEX
    )

    assert report.improvement_percent == 81.4

    assert report.cost_before == 120.0

    assert report.cost_after == 22.3

    assert report.plan_changed