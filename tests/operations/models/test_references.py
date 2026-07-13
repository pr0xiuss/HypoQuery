from dataclasses import FrozenInstanceError

import pytest

from backend.operations.models.references import (
    RecommendationReference,
)
from backend.optimization.recommendation.models.recommendation_key import (
    RecommendationKey,
)


def test_recommendation_reference_creation() -> None:
    key = RecommendationKey(
        category="INDEX",
        target="orders(customer_id)",
        action="CREATE",
    )

    reference = RecommendationReference(
        key=key,
        recommendation_code="CREATE_INDEX",
    )

    assert reference.key == key
    assert reference.recommendation_code == "CREATE_INDEX"
    assert reference.recommendation_version == 1


def test_recommendation_reference_is_immutable() -> None:
    key = RecommendationKey(
        category="INDEX",
        target="orders(customer_id)",
        action="CREATE",
    )

    reference = RecommendationReference(
        key=key,
        recommendation_code="CREATE_INDEX",
    )

    with pytest.raises(FrozenInstanceError):
        reference.recommendation_code = "UPDATED"