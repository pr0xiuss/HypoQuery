from __future__ import annotations

from backend.optimization.reporting.models.validation_report import (
    ValidationReport,
)
from backend.optimization.validation.models.validation import (
    Validation,
)


class ValidationReportBuilder:
    """
    Builds ValidationReport objects.
    """

    def build(
        self,
        validation: Validation | None,
    ) -> ValidationReport:

        if validation is None:

            return ValidationReport(
                status=None,
                validation_type=None,
                improvement_percent=0.0,
                cost_before=0.0,
                cost_after=0.0,
                plan_changed=False,
            )

        metrics = validation.metrics

        return ValidationReport(
            status=validation.status,
            validation_type=validation.validation_type,
            improvement_percent=(
                metrics.improvement_percent
                if metrics is not None
                else 0.0
            ),
            cost_before=(
                metrics.before_cost
                if metrics is not None
                else 0.0
            ),
            cost_after=(
                metrics.after_cost
                if metrics is not None
                else 0.0
            ),
            plan_changed=(
                metrics.plan_changed
                if metrics is not None
                else False
            ),
        )