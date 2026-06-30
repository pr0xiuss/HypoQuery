from infrastructure.postgres.scripts.observability.analyzers.rules.shared_buffer_rule import (
    SharedBufferRule,
)
from infrastructure.postgres.scripts.observability.models.execution_plan import (
    ExecutionPlan,
)


def test_detect_high_shared_reads():

    plan = ExecutionPlan(
        node_type="Seq Scan",
        estimated_rows=100,
        actual_rows=100,
        startup_cost=0,
        total_cost=20,
        planning_time_ms=1,
        execution_time_ms=2,
        shared_hit_blocks=0,
        shared_read_blocks=500,
        temp_read_blocks=0,
        temp_written_blocks=0,
        children=[],
    )

    findings = SharedBufferRule().check(plan)

    assert len(findings) == 1


def test_ignore_low_shared_reads():

    plan = ExecutionPlan(
        node_type="Seq Scan",
        estimated_rows=100,
        actual_rows=100,
        startup_cost=0,
        total_cost=20,
        planning_time_ms=1,
        execution_time_ms=2,
        shared_hit_blocks=0,
        shared_read_blocks=5,
        temp_read_blocks=0,
        temp_written_blocks=0,
        children=[],
    )

    assert SharedBufferRule().check(plan) == []