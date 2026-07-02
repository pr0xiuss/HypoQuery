from datetime import UTC, datetime

from backend.execution.contracts.fingerprint import (
    QueryFingerprint,
)

from backend.ingestion.selection.analysis_candidate import (
    AnalysisCandidate,
)
from backend.ingestion.selection.scoring_policy import (
    ScoringPolicy,
)


def make_candidate() -> AnalysisCandidate:
    return AnalysisCandidate(
        fingerprint=QueryFingerprint(
            normalized_sql="SELECT 1",
            hash="hash",
        ),
        database="postgres",
        schema="public",
        query="SELECT 1",
        execution_count=100,
        average_duration_ms=50,
        total_duration_ms=5000,
        rows_processed=200,
        shared_blocks_read=20,
        temp_blocks_written=10,
        last_seen=datetime.now(UTC),
    )


def test_score_breakdown():
    policy = ScoringPolicy()

    score = policy.score(
        make_candidate(),
    )

    assert score.duration_score == 20.0
    assert score.frequency_score == 30.0
    assert score.resource_score == 6.0
    assert score.rows_score == 20.0

    assert score.total == 76.0