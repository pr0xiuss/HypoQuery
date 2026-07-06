from backend.optimization.recommendation.models.category import (
    RecommendationCategory,
)
from backend.optimization.recommendation.models.location import (
    RecommendationLocation,
)
from backend.optimization.recommendation.models.metadata import (
    RecommendationMetadata,
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
from backend.optimization.validation.builders.index_statement_builder import (
    IndexStatementBuilder,
)


def test_build_create_index_statement():

    builder = IndexStatementBuilder()

    recommendation = Recommendation(
        category=RecommendationCategory.INDEX,
        code="CREATE_INDEX",
        key=RecommendationKey(
            category="index",
            target="customers",
            action="create",
        ),
        title="Create Index",
        description="",
        priority=RecommendationPriority.HIGH,
        location=RecommendationLocation(
            relation="customers",
            schema="public",
        ),
        metadata=RecommendationMetadata(
            attributes={
                "filter_columns": [
                    "customer_id",
                ],
            },
        ),
    )

    statement = builder.build(
        recommendation,
    )

    assert (
        statement
        == "CREATE INDEX idx_customers_customer_id "
        "ON customers (customer_id)"
    )