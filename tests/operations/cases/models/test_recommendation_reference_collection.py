from backend.operations.cases.models.recommendation_reference_collection import (
    RecommendationReferenceCollection,
)
from backend.operations.models.references import (
    RecommendationReference,
)
from backend.optimization.recommendation.models.recommendation_key import (
    RecommendationKey,
)


def build_reference() -> RecommendationReference:
    return RecommendationReference(
        key=RecommendationKey(
            category="INDEX",
            target="orders(customer_id)",
            action="CREATE",
        ),
        recommendation_code="CREATE_INDEX",
    )


def test_collection_starts_empty() -> None:
    collection = RecommendationReferenceCollection()

    assert len(collection) == 0


def test_add_recommendation() -> None:
    collection = RecommendationReferenceCollection()

    reference = build_reference()

    collection.add(reference)

    assert len(collection) == 1
    assert collection.contains(reference)


def test_duplicate_recommendations_are_ignored() -> None:
    collection = RecommendationReferenceCollection()

    reference = build_reference()

    collection.add(reference)
    collection.add(reference)

    assert len(collection) == 1


def test_collection_supports_iteration() -> None:
    collection = RecommendationReferenceCollection()

    reference = build_reference()

    collection.add(reference)

    assert list(collection) == [reference]


def test_collection_supports_indexing() -> None:
    collection = RecommendationReferenceCollection()

    reference = build_reference()

    collection.add(reference)

    assert collection[0] == reference