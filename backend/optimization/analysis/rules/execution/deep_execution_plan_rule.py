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
from backend.shared.constants import DEEP_EXECUTION_PLAN_DEPTH


class DeepExecutionPlanRule(AnalysisRule):
    """
    Detects execution plans with excessive nesting depth.
    """

    def __init__(
        self,
        traverser: ExecutionPlanTraverser,
    ) -> None:
        self._traverser = traverser

    @property
    def name(self) -> str:
        return "deep_execution_plan"

    def analyze(
        self,
        context: AnalysisContext,
    ) -> FindingCollection:

        findings = FindingCollection()

        max_depth = 0

        for _, depth in self._traverser.depth_first_with_depth(
            context.execution_plan,
        ):
            max_depth = max(max_depth, depth)

        if max_depth < DEEP_EXECUTION_PLAN_DEPTH:
            return findings

        findings.add(
            Finding(
                category=FindingCategory.EXECUTION,
                code="DEEP_EXECUTION_PLAN",
                title="Deep Execution Plan",
                description=(
                    f"Execution plan depth is {max_depth}, "
                    "which may indicate a complex execution strategy."
                ),
                severity=FindingSeverity.MEDIUM,
                location=FindingLocation(),
                metadata=FindingMetadata(
                    attributes={
                        "depth": max_depth,
                    }
                ),
            )
        )

        return findings