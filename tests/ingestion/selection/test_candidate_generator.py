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


def make_candidate() -> AnalysisCandidate:
    return AnalysisCandidate(
        fingerprint=QueryFingerprint(
            normalized_sql="SELECT 1",
            hash="hash",
        ),
        database="postgres",
        schema="public",
        query="SELECT 1",
        execution_count=10,
        average_duration_ms=5,
        total_duration_ms=50,
        rows_processed=100,
        shared_blocks_read=10,
        temp_blocks_written=0,
        last_seen=datetime.now(UTC),
    )


def test_generate_candidates():
    generator = CandidateGenerator()

    candidate = make_candidate()

    result = generator.generate(
        [candidate],
    )

    assert len(result) == 1
    assert result[0] is candidate


def test_empty_workload():
    generator = CandidateGenerator()

    assert generator.generate([]) == []