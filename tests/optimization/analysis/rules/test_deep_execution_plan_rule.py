from backend.optimization.analysis.context import AnalysisContext
from backend.optimization.analysis.rules.execution.deep_execution_plan_rule import (
    DeepExecutionPlanRule,
)
from backend.optimization.analysis.traversal.execution_plan_traverser import (
    ExecutionPlanTraverser,
)
from backend.optimization.models.execution_plan import ExecutionPlan
from backend.shared.constants import DEEP_EXECUTION_PLAN_DEPTH


def build_chain(depth: int) -> ExecutionPlan:

    root = ExecutionPlan(
        node_type="Seq Scan",
    )

    current = root

    for _ in range(depth - 1):

        child = ExecutionPlan(
            node_type="Nested Loop",
        )

        current.children.append(child)

        current = child

    return root


def test_detects_deep_execution_plan():

    plan = build_chain(
        DEEP_EXECUTION_PLAN_DEPTH + 1,
    )

    rule = DeepExecutionPlanRule(
        ExecutionPlanTraverser(),
    )

    findings = rule.analyze(
        AnalysisContext(
            execution_plan=plan,
        )
    )

    assert len(findings) == 1

    finding = next(iter(findings))

    assert finding.code == "DEEP_EXECUTION_PLAN"
    assert finding.title == "Deep Execution Plan"


def test_ignores_shallow_execution_plan():

    plan = build_chain(
        DEEP_EXECUTION_PLAN_DEPTH,
    )

    rule = DeepExecutionPlanRule(
        ExecutionPlanTraverser(),
    )

    findings = rule.analyze(
        AnalysisContext(
            execution_plan=plan,
        )
    )

    assert findings.is_empty()