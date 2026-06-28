from infrastructure.postgres.scripts.observability.analyzers.rules.index_scan_rule import (
    IndexScanRule,
)
from infrastructure.postgres.scripts.observability.models.execution_plan import (
    ExecutionPlan,
)


def test_detect_index_scan():

    plan = ExecutionPlan(
        node_type="Index Scan",
        estimated_rows=100,
        actual_rows=100,
        startup_cost=0,
        total_cost=10,
        planning_time_ms=1,
        execution_time_ms=2,
        shared_hit_blocks=0,
        shared_read_blocks=0,
        temp_read_blocks=0,
        temp_written_blocks=0,
        children=[],
    )

    findings = IndexScanRule().check(plan)

    assert len(findings) == 1


def test_ignore_other_nodes():

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

    assert IndexScanRule().check(plan) == []