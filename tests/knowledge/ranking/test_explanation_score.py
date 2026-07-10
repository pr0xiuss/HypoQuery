from backend.knowledge.models.explanation_priority import (
    ExplanationPriority,
)
from backend.knowledge.ranking.explanation_score import (
    ExplanationScore,
)


def test_explanation_score():

    score = ExplanationScore(
        priority=ExplanationPriority.PRIMARY,
        score=0.95,
    )

    assert (
        score.priority
        == ExplanationPriority.PRIMARY
    )

    assert (
        score.score
        == 0.95
    )