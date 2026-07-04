from __future__ import annotations

from backend.optimization.analysis.context import AnalysisContext
from backend.optimization.analysis.models.categories import FindingCategory
from backend.optimization.analysis.models.finding import Finding
from backend.optimization.analysis.models.finding_collection import FindingCollection
from backend.optimization.analysis.models.location import FindingLocation
from backend.optimization.analysis.models.metadata import FindingMetadata
from backend.optimization.analysis.models.severity import FindingSeverity
from backend.optimization.analysis.rules.base_rule import AnalysisRule
from backend.optimization.analysis.traversal.execution_plan_traverser import (
    ExecutionPlanTraverser,
)
from backend.shared.constants import CARDINALITY_MISMATCH_FACTOR


class CardinalityMismatchRule(AnalysisRule):
    """
    Detects significant differences between planner estimates
    and actual execution results.
    """

    def __init__(
        self,
        traverser: ExecutionPlanTraverser,
    ) -> None:
        self._traverser = traverser

    @property
    def name(self) -> str:
        return "cardinality_mismatch"

    def analyze(
        self,
        context: AnalysisContext,
    ) -> FindingCollection:

        findings = FindingCollection()

        for node in self._traverser.depth_first(context.execution_plan):

            estimated = max(node.estimated_rows, 1)
            actual = max(node.actual_rows, 1)

            ratio = max(
                actual / estimated,
                estimated / actual,
            )

            if ratio < CARDINALITY_MISMATCH_FACTOR:
                continue

            findings.add(
                Finding(
                    category=FindingCategory.EXECUTION,
                    code="CARDINALITY_MISMATCH",
                    title="Cardinality Mismatch",
                    description=(
                        "Planner row estimate differs significantly "
                        "from observed execution."
                    ),
                    severity=FindingSeverity.HIGH,
                    location=FindingLocation(
                        relation=node.relation_name,
                        schema=node.schema_name,
                    ),
                    metadata=FindingMetadata(
                        attributes={
                            "estimated_rows": estimated,
                            "actual_rows": actual,
                            "ratio": round(ratio, 2),
                            "node_type": node.node_type,
                        }
                    ),
                )
            )

        return findings