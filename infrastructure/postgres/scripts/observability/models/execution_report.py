from dataclasses import dataclass


@dataclass(slots=True)
class ExecutionReport:

    query_id: str

    query_name: str

    execution_time_ms: float

    rows_returned: int

    success: bool

    error: str | None

    planning_time_ms: float | None

    shared_hit_blocks: int | None

    shared_read_blocks: int | None

    temp_read_blocks: int | None

    temp_written_blocks: int | None

    execution_plan: dict | None