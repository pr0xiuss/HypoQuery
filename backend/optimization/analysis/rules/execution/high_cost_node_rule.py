from __future__ import annotations

from backend.optimization.analysis.context import AnalysisContext
from backend.optimization.analysis.models.categories import FindingCategory
from backend.optimization.analysis.models.finding import Finding
from backend.optimization.analysis.models.finding_collection import (
    FindingCollection,
)
from backend.optimization.analysis.models.location import FindingLocation
from backend.optimization.analysis.models.metadata import FindingMetadata
from backend.optimization.analysis.models.severity import FindingSeverity
from backend.optimization.analysis.rules.base_rule import AnalysisRule
from backend.optimization.analysis.traversal.execution_plan_traverser import (
    ExecutionPlanTraverser,
)
from backend.shared.constants import HIGH_COST_NODE_THRESHOLD


class HighCostNodeRule(AnalysisRule):
    """
    Detects execution plan nodes whose estimated planner cost is unusually high.
    """

    def __init__(
        self,
        traverser: ExecutionPlanTraverser,
    ) -> None:
        self._traverser = traverser

    @property
    def name(self) -> str:
        return "high_cost_node"

    def analyze(
        self,
        context: AnalysisContext,
    ) -> FindingCollection:

        findings = FindingCollection()

        for node in self._traverser.depth_first(context.execution_plan):

            if node.total_cost < HIGH_COST_NODE_THRESHOLD:
                continue

            findings.add(
                Finding(
                    category=FindingCategory.EXECUTION,
                    code="HIGH_COST_NODE",
                    title="High Cost Operation",
                    description=(
                        f"Execution plan node has a high estimated cost "
                        f"({node.total_cost:.2f})."
                    ),
                    severity=FindingSeverity.MEDIUM,
                    location=FindingLocation(
                        relation=node.relation_name,
                        schema=node.schema_name,
                    ),
                    metadata=FindingMetadata(
                        attributes={
                            "node_type": node.node_type,
                            "startup_cost": node.startup_cost,
                            "total_cost": node.total_cost,
                            "estimated_rows": node.estimated_rows,
                            "actual_rows": node.actual_rows,
                        }
                    ),
                )
            )

        return findings