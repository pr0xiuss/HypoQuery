from datetime import UTC, datetime

from backend.execution.contracts.fingerprint import (
    QueryFingerprint,
)

from backend.ingestion.selection.analysis_candidate import (
    AnalysisCandidate,
)
from backend.ingestion.selection.candidate_generator import (
    CandidateGenerator,
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


def test_candidate_selection_flow():
    workload = [
        make_candidate(50, 20),
        make_candidate(500, 200),
        make_candidate(10, 5),
    ]

    generator = CandidateGenerator()

    candidates = generator.generate(
        workload,
    )

    engine = SelectionEngine(
        ScoringPolicy(),
    )

    selected = engine.select(
        candidates,
        limit=2,
    )

    assert len(selected) == 2
    assert selected[0].average_duration_ms == 500
    assert selected[1].average_duration_ms == 50