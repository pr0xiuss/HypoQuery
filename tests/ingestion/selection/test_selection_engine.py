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
from backend.ingestion.selection.selection_engine import (
    SelectionEngine,
)


def make_candidate(
    duration: float,
    executions: int,
) -> AnalysisCandidate:
    return AnalysisCandidate(
        fingerprint=QueryFingerprint(
            normalized_sql="SELECT 1",
            hash=str(duration),
        ),
        database="postgres",
        schema="public",
        query="SELECT 1",
        execution_count=executions,
        average_duration_ms=duration,
        total_duration_ms=duration * executions,
        rows_processed=100,
        shared_blocks_read=10,
        temp_blocks_written=0,
        last_seen=datetime.now(UTC),
    )


def test_select_highest_scores():
    engine = SelectionEngine(
        ScoringPolicy(),
    )

    low = make_candidate(10, 10)
    medium = make_candidate(100, 50)
    high = make_candidate(500, 100)

    selected = engine.select(
        [medium, low, high],
        limit=2,
    )

    assert len(selected) == 2
    assert selected[0] is high
    assert selected[1] is medium


def test_empty_candidates():
    engine = SelectionEngine(
        ScoringPolicy(),
    )

    assert engine.select([], 5) == []


def test_limit_larger_than_candidates():
    engine = SelectionEngine(
        ScoringPolicy(),
    )

    candidate = make_candidate(50, 10)

    selected = engine.select(
        [candidate],
        limit=10,
    )

    assert selected == [candidate]