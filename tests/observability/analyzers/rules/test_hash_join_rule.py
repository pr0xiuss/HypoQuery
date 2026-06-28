from infrastructure.postgres.scripts.observability.analyzers.rules.hash_join_rule import (
    HashJoinRule,
)
from infrastructure.postgres.scripts.observability.models.execution_plan import (
    ExecutionPlan,
)


def test_detect_hash_join():

    plan = ExecutionPlan(
        node_type="Hash Join",
        estimated_rows=100,
        actual_rows=100,
        startup_cost=0,
        total_cost=50,
        planning_time_ms=1,
        execution_time_ms=2,
        shared_hit_blocks=0,
        shared_read_blocks=0,
        temp_read_blocks=0,
        temp_written_blocks=0,
        children=[],
    )

    findings = HashJoinRule().check(plan)

    assert len(findings) == 1
    assert findings[0].issue.startswith("Hash Join")


def test_ignore_non_hash_join():

    plan = ExecutionPlan(
        node_type="Seq Scan",
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

    assert HashJoinRule().check(plan) == []