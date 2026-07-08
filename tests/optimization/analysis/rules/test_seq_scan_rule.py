from backend.optimization.analysis.context import AnalysisContext
from backend.optimization.analysis.rules.execution.seq_scan_rule import SeqScanRule
from backend.optimization.analysis.traversal.execution_plan_traverser import ExecutionPlanTraverser
from backend.optimization.analysis.parsers.predicate_parser import PredicateParser
from backend.optimization.models.execution_plan import ExecutionPlan
from backend.shared.constants import LARGE_TABLE_SCAN_ROWS


def test_detects_large_seq_scan():

    plan = ExecutionPlan(
        node_type="Seq Scan",
        relation_name="users",
        actual_rows=LARGE_TABLE_SCAN_ROWS + 1,
        estimated_rows=LARGE_TABLE_SCAN_ROWS + 1,
    )

    rule = SeqScanRule(
        ExecutionPlanTraverser(),
        PredicateParser()
    )

    findings = rule.analyze(
        AnalysisContext(
            execution_plan=plan,
        )
    )

    assert len(findings) == 1

    finding = next(iter(findings))

    assert finding.code == "LARGE_TABLE_SCAN"
    assert finding.title == "Large Sequential Scan"


def test_ignores_small_seq_scan():

    plan = ExecutionPlan(
        node_type="Seq Scan",
        relation_name="users",
        actual_rows=LARGE_TABLE_SCAN_ROWS - 1,
    )

    rule = SeqScanRule(
        ExecutionPlanTraverser(),
        PredicateParser()
    )

    findings = rule.analyze(
        AnalysisContext(
            execution_plan=plan,
        )
    )

    assert findings.is_empty()