from dataclasses import dataclass, field


@dataclass(slots=True)
class ExecutionPlan:

    node_type: str

    relation_name: str | None = None

    schema_name: str | None = None

    alias: str | None = None

    parent_relationship: str | None = None

    join_type: str | None = None

    index_name: str | None = None

    hash_condition: str | None = None

    filter_condition: str | None = None

    estimated_rows: int = 0

    actual_rows: int = 0

    startup_cost: float = 0.0

    total_cost: float = 0.0

    planning_time_ms: float = 0.0

    execution_time_ms: float = 0.0

    shared_hit_blocks: int = 0

    shared_read_blocks: int = 0

    temp_read_blocks: int = 0

    temp_written_blocks: int = 0

    children: list["ExecutionPlan"] = field(default_factory=list)
