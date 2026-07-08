from __future__ import annotations

from datetime import UTC, datetime

from backend.optimization.validation.context import (
    ValidationContext,
)
from backend.optimization.validation.models.validation_result import (
    ValidationResult,
)
from backend.optimization.validation.registry.validator_registry import (
    ValidatorRegistry,
)


class ValidationEngine:
    """
    Coordinates execution of all registered recommendation validators.
    """

    def __init__(self, registry: ValidatorRegistry,) -> None:

        self._registry = registry

    def validate(self, context: ValidationContext,) -> ValidationResult:

        result = ValidationResult()

        for recommendation in context.recommendation_result.recommendations:

            for validator in self._registry:

                if (
                    recommendation.code
                    not in validator.supported_codes
                ):
                    continue

                validation = validator.validate(
                    context,
                    recommendation,
                )

                if validation is not None:

                    result.validations.add(
                        validation,
                    )

        result.completed_at = datetime.now(
            UTC,
        )

        return result