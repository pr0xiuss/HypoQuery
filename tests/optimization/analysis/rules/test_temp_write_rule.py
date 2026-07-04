from backend.optimization.analysis.context import AnalysisContext
from backend.optimization.analysis.rules.execution.temp_write_rule import (
    TempWriteRule,
)
from backend.optimization.analysis.traversal.execution_plan_traverser import (
    ExecutionPlanTraverser,
)
from backend.optimization.models.execution_plan import ExecutionPlan
from backend.shared.constants import TEMP_WRITTEN_BLOCKS_THRESHOLD


def test_detects_temp_disk_writes():

    plan = ExecutionPlan(
        node_type="Sort",
        temp_written_blocks=TEMP_WRITTEN_BLOCKS_THRESHOLD + 1,
    )

    rule = TempWriteRule(
        ExecutionPlanTraverser(),
    )

    findings = rule.analyze(
        AnalysisContext(
            execution_plan=plan,
        )
    )

    assert len(findings) == 1

    finding = next(iter(findings))

    assert finding.code == "TEMP_DISK_WRITES"
    assert finding.title == "Temporary Disk Writes"


def test_ignores_zero_temp_disk_writes():

    plan = ExecutionPlan(
        node_type="Sort",
        temp_written_blocks=TEMP_WRITTEN_BLOCKS_THRESHOLD,
    )

    rule = TempWriteRule(
        ExecutionPlanTraverser(),
    )

    findings = rule.analyze(
        AnalysisContext(
            execution_plan=plan,
        )
    )

    assert findings.is_empty()  