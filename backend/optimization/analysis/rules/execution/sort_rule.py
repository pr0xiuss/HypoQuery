from __future__ import annotations

from backend.shared.constants import (
    LARGE_SORT_COST,
)
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


class SortRule(AnalysisRule):
    """
    Detects expensive sort operations.
    """

    def __init__(
        self,
        traverser: ExecutionPlanTraverser,
    ) -> None:
        self._traverser = traverser

    @property
    def name(self) -> str:
        return "sort"

    def analyze(
        self,
        context: AnalysisContext,
    ) -> FindingCollection:

        findings = FindingCollection()

        for node in self._traverser.depth_first(context.execution_plan):

            if node.node_type != "Sort":
                continue

            if node.total_cost < LARGE_SORT_COST:
                continue

            findings.add(
                Finding(
                    category=FindingCategory.EXECUTION,
                    code="EXPENSIVE_SORT",
                    title="Expensive Sort",
                    description=(
                        f"Expensive sort operation detected "
                        f"(cost={node.total_cost:.2f})."
                    ),
                    severity=FindingSeverity.MEDIUM,
                    location=FindingLocation(
                        relation=node.relation_name,
                        schema=node.schema_name,
                    ),
                    metadata=FindingMetadata(
                        attributes={
                            "startup_cost": node.startup_cost,
                            "total_cost": node.total_cost,
                            "estimated_rows": node.estimated_rows,
                            "actual_rows": node.actual_rows,
                            "temp_written_blocks": node.temp_written_blocks,
                        }
                    ),
                )
            )

        return findings