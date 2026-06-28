from dataclasses import dataclass


@dataclass(slots=True)
class QueryResult:

    query_id: str

    query_name: str

    execution_time_ms: float

    rows_returned: int

    success: bool

    error: str | None
