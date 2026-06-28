from infrastructure.postgres.scripts.observability.analyzers.rules.nested_loop_rule import (
    NestedLoopRule,
)
from infrastructure.postgres.scripts.observability.models.execution_plan import (
    ExecutionPlan,
)


def test_detect_nested_loop():

    plan = ExecutionPlan(
        node_type="Nested Loop",
        estimated_rows=100,
        actual_rows=100,
        startup_cost=0,
        total_cost=100,
        planning_time_ms=1,
        execution_time_ms=2,
        shared_hit_blocks=0,
        shared_read_blocks=0,
        temp_read_blocks=0,
        temp_written_blocks=0,
        children=[],
    )

    findings = NestedLoopRule().check(plan)

    assert len(findings) == 1


def test_ignore_other_nodes():

    plan = ExecutionPlan(
        node_type="Hash Join",
        estimated_rows=100,
        actual_rows=100,
        startup_cost=0,
        total_cost=20,
        planning_time_ms=1,
        execution_time_ms=2,
        shared_hit_blocks=0,
        shared_read_blocks=0,
        temp_read_blocks=0,
        temp_written_blocks=0,
        children=[],
    )

    assert NestedLoopRule().check(plan) == []