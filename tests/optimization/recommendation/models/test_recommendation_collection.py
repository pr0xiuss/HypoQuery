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


def create_recommendation() -> Recommendation:

    return Recommendation(
        category=RecommendationCategory.INDEX,
        code="CREATE_INDEX",
        key=RecommendationKey(
            category=RecommendationCategory.INDEX,
            target="customers",
            action="create",
        ),
        title="Create Index",
        description="Create an index.",
        priority=RecommendationPriority.HIGH,
    )


def test_collection_add():

    collection = RecommendationCollection()

    collection.add(
        create_recommendation(),
    )

    assert len(collection) == 1


def test_collection_extend():

    left = RecommendationCollection()

    right = RecommendationCollection()

    right.add(
        create_recommendation(),
    )

    left.extend(
        right,
    )

    assert len(left) == 1


def test_collection_empty():

    collection = RecommendationCollection()

    assert collection.is_empty()