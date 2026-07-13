from dataclasses import FrozenInstanceError

import pytest

from backend.operations.models.value_objects import (
    ConfidenceScore,
)


def test_confidence_score_creation() -> None:
    score = ConfidenceScore(0.95)

    assert score.value == 0.95


def test_confidence_score_equality() -> None:
    left = ConfidenceScore(0.8)
    right = ConfidenceScore(0.8)

    assert left == right


def test_confidence_score_is_immutable() -> None:
    score = ConfidenceScore(0.9)

    with pytest.raises(FrozenInstanceError):
        score.value = 0.5