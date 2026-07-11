from backend.knowledge.retrieval.ranking.retrieval_score import (
    RetrievalScore,
)


def test_retrieval_score():

    score = RetrievalScore(
        confidence=0.9,
        relevance=0.8,
        total=1.7,
    )

    assert score.confidence == 0.9

    assert score.relevance == 0.8

    assert score.total == 1.7