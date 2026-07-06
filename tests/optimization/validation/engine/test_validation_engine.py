from backend.optimization.recommendation.models.category import (
    RecommendationCategory,
)
from backend.optimization.recommendation.models.priority import (
    RecommendationPriority,
)
from backend.optimization.recommendation.models.recommendation import (
    Recommendation,
)
from backend.optimization.recommendation.models.recommendation_collection import (
    RecommendationCollection,
)
from backend.optimization.recommendation.models.recommendation_key import (
    RecommendationKey,
)
from backend.optimization.validation.context import (
    ValidationContext,
)
from backend.optimization.validation.engine import (
    ValidationEngine,
)
from backend.optimization.validation.models.validation import (
    Validation,
)
from backend.optimization.validation.models.validation_result import (
    ValidationResult,
)
from backend.optimization.validation.models.validation_status import (
    ValidationStatus,
)
from backend.optimization.validation.models.validation_type import (
    ValidationType,
)
from backend.optimization.validation.registry.validator_registry import (
    ValidatorRegistry,
)
from backend.optimization.validation.validators.base_validator import (
    RecommendationValidator,
)
from backend.optimization.models.execution_plan import (
    ExecutionPlan,
)


class DummyValidator(RecommendationValidator):

    @property
    def name(self) -> str:
        return "dummy"

    @property
    def supported_codes(self) -> set[str]:
        return {"CREATE_INDEX"}

    def validate(
        self,
        context,
        recommendation,
    ):

        return Validation(
            recommendation=recommendation,
            status=ValidationStatus.VALIDATED,
            validation_type=ValidationType.HYPOTHETICAL_INDEX,
            metrics=None,
            validation_artifact=None,
        )


def test_engine_dispatches_supported_validator():

    recommendation = Recommendation(
        category=RecommendationCategory.INDEX,
        code="CREATE_INDEX",
        key=RecommendationKey(
            category="index",
            target="users",
            action="create",
        ),
        title="",
        description="",
        priority=RecommendationPriority.HIGH,
    )

    recommendations = RecommendationCollection()

    recommendations.add(
        recommendation,
    )

    context = ValidationContext(
        execution_plan=ExecutionPlan(
            node_type="Seq Scan",
        ),
        recommendation_result=recommendations,
        normalized_sql="SELECT 1;",
        fingerprint=None,
    )

    registry = ValidatorRegistry()

    registry.register(
        DummyValidator(),
    )

    engine = ValidationEngine(
        registry,
    )

    result = engine.validate(
        context,
    )

    assert isinstance(
        result,
        ValidationResult,
    )

    assert len(
        result.validations,
    ) == 1