from backend.optimization.analysis.context import AnalysisContext
from backend.optimization.analysis.rules.execution.shared_buffer_rule import (
    SharedBufferRule,
)
from backend.optimization.analysis.traversal.execution_plan_traverser import (
    ExecutionPlanTraverser,
)
from backend.optimization.models.execution_plan import ExecutionPlan
from backend.shared.constants import HIGH_SHARED_READ_BLOCKS


def test_detects_high_shared_buffer_reads():

    plan = ExecutionPlan(
        node_type="Seq Scan",
        shared_read_blocks=HIGH_SHARED_READ_BLOCKS + 1,
    )

    rule = SharedBufferRule(
        ExecutionPlanTraverser(),
    )

    findings = rule.analyze(
        AnalysisContext(
            execution_plan=plan,
        )
    )

    assert len(findings) == 1

    finding = next(iter(findings))

    assert finding.code == "HIGH_SHARED_READS"
    assert finding.title == "High Shared Buffer Reads"


def test_ignores_normal_shared_buffer_reads():

    plan = ExecutionPlan(
        node_type="Seq Scan",
        shared_read_blocks=HIGH_SHARED_READ_BLOCKS,
    )

    rule = SharedBufferRule(
        ExecutionPlanTraverser(),
    )

    findings = rule.analyze(
        AnalysisContext(
            execution_plan=plan,
        )
    )

    assert findings.is_empty()