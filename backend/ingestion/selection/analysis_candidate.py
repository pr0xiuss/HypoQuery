from dataclasses import dataclass
from datetime import datetime

from backend.execution.contracts.fingerprint import (
    QueryFingerprint,
)


@dataclass(slots=True)
class AnalysisCandidate:
    """
    Represents a query that is eligible for optimization analysis.
    """

    fingerprint: QueryFingerprint

    database: str

    schema: str

    query: str

    execution_count: int

    average_duration_ms: float

    total_duration_ms: float

    rows_processed: int

    shared_blocks_read: int

    temp_blocks_written: int

    last_seen: datetime