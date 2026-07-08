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
from backend.shared.constants import LARGE_HASH_AGGREGATE_ROWS


class HashAggregateRule(AnalysisRule):
    """
    Detects expensive hash aggregate operations.
    """

    def __init__(
        self,
        traverser: ExecutionPlanTraverser,
    ) -> None:
        self._traverser = traverser

    @property
    def name(self) -> str:
        return "hash_aggregate"

    def analyze(
        self,
        context: AnalysisContext,
    ) -> FindingCollection:

        findings = FindingCollection()

        for node in self._traverser.depth_first(context.execution_plan):

            if node.node_type != "HashAggregate":
                continue

            if node.actual_rows < LARGE_HASH_AGGREGATE_ROWS:
                continue

            findings.add(
                Finding(
                    category=FindingCategory.EXECUTION,
                    code="LARGE_HASH_AGGREGATE",
                    title="Large Hash Aggregate",
                    description=(
                        f"Large hash aggregate processed "
                        f"{node.actual_rows:,} rows."
                    ),
                    severity=FindingSeverity.MEDIUM,
                    location=FindingLocation(
                        relation=node.relation_name,
                        schema=node.schema_name,
                    ),
                    metadata=FindingMetadata(
                        attributes={
                            "actual_rows": node.actual_rows,
                            "estimated_rows": node.estimated_rows,
                            "startup_cost": node.startup_cost,
                            "total_cost": node.total_cost,
                        }
                    ),
                )
            )

        return findings