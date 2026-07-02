from backend.ingestion.selection.candidate_score import (
    CandidateScore,
)


def test_total_score():
    score = CandidateScore(
        duration_score=40,
        frequency_score=30,
        resource_score=20,
        rows_score=10,
    )

    assert score.total == 100