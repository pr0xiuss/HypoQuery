from backend.optimization.analysis.analyzers.execution_analyzer import (
    ExecutionAnalyzer,
)
from backend.optimization.analysis.context import AnalysisContext
from backend.optimization.analysis.registry.rule_registry import RuleRegistry
from backend.optimization.analysis.rules.execution.seq_scan_rule import SeqScanRule
from backend.optimization.analysis.traversal.execution_plan_traverser import ExecutionPlanTraverser
from backend.optimization.analysis.parsers.predicate_parser import PredicateParser
from backend.optimization.models.execution_plan import ExecutionPlan
from backend.shared.constants import LARGE_TABLE_SCAN_ROWS


def test_execution_analyzer_runs_registered_rules():

    registry = RuleRegistry()

    registry.register(
        SeqScanRule(
            ExecutionPlanTraverser(),
            PredicateParser()
        )
    )

    analyzer = ExecutionAnalyzer(
        registry,
    )

    plan = ExecutionPlan(
        node_type="Seq Scan",
        actual_rows=LARGE_TABLE_SCAN_ROWS,
    )

    findings = analyzer.analyze(
        AnalysisContext(
            execution_plan=plan,
        )
    )

    assert len(findings) == 1

    finding = next(iter(findings))

    assert finding.code == "LARGE_TABLE_SCAN"