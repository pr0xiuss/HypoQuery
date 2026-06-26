from dataclasses import dataclass


@dataclass(slots=True)
class ExecutionPlan:

    node_type: str

    estimated_rows: int

    actual_rows: int

    startup_cost: float

    total_cost: float

    planning_time_ms: float

    execution_time_ms: float

    shared_hit_blocks: int

    shared_read_blocks: int

    temp_read_blocks: int

    temp_written_blocks: int