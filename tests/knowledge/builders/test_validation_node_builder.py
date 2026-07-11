from backend.knowledge.models.enums import KnowledgeNodeType
from backend.knowledge.projection.builders.validation_node_builder import (
    ValidationNodeBuilder,
)
from backend.optimization.recommendation.models.category import (
    RecommendationCategory,
)
from backend.optimization.recommendation.models.priority import (
    RecommendationPriority,
)
from backend.optimization.recommendation.models.recommendation import (
    Recommendation,
)
from backend.optimization.recommendation.models.recommendation_key import (
    RecommendationKey,
)
from backend.optimization.validation.models.validation import (
    Validation,
)
from backend.optimization.validation.models.validation_status import (
    ValidationStatus,
)
from backend.optimization.validation.models.validation_type import (
    ValidationType,
)


def test_build_validation_node() -> None:

    builder = ValidationNodeBuilder()

    recommendation = Recommendation(
        category=RecommendationCategory.INDEX,
        code="CREATE_INDEX",
        key=RecommendationKey(
            category="index",
            target="users",
            action="create",
        ),
        title="Create Index",
        description="Create an index.",
        priority=RecommendationPriority.HIGH,
    )

    validation = Validation(
        recommendation=recommendation,
        status=ValidationStatus.VALIDATED,
        validation_type=ValidationType.HYPOTHETICAL_INDEX,
    )

    node = builder.build(validation)

    assert node.type == KnowledgeNodeType.VALIDATION
    assert node.properties["status"] == "VALIDATED"
    assert node.properties["recommendation"] == "CREATE_INDEX"