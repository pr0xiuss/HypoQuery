from __future__ import annotations

from backend.optimization.analysis.analyzers.execution_analyzer import (
    ExecutionAnalyzer,
)
from backend.optimization.analysis.registry.rule_registry import RuleRegistry
from backend.optimization.analysis.rules.execution.cardinality_mismatch_rule import (
    CardinalityMismatchRule,
)
from backend.optimization.analysis.rules.execution.deep_execution_plan_rule import (
    DeepExecutionPlanRule,
)
from backend.optimization.analysis.rules.execution.hash_aggregate_rule import (
    HashAggregateRule,
)
from backend.optimization.analysis.rules.execution.high_cost_node_rule import (
    HighCostNodeRule,
)
from backend.optimization.analysis.rules.execution.nested_loop_rule import (
    NestedLoopRule,
)
from backend.optimization.analysis.rules.execution.seq_scan_rule import (
    SeqScanRule,
)
from backend.optimization.analysis.rules.execution.shared_buffer_rule import (
    SharedBufferRule,
)
from backend.optimization.analysis.rules.execution.sort_rule import (
    SortRule,
)
from backend.optimization.analysis.rules.execution.temp_write_rule import (
    TempWriteRule,
)
from backend.optimization.analysis.traversal.execution_plan_traverser import (
    ExecutionPlanTraverser,
)


def build_execution_analyzer() -> ExecutionAnalyzer:
    """
    Composition root for the execution analysis domain.
    """

    traverser = ExecutionPlanTraverser()

    registry = RuleRegistry()

    registry.register(SeqScanRule(traverser))
    registry.register(SharedBufferRule(traverser))
    registry.register(TempWriteRule(traverser))
    registry.register(SortRule(traverser))
    registry.register(NestedLoopRule(traverser))
    registry.register(HashAggregateRule(traverser))
    registry.register(CardinalityMismatchRule(traverser))
    registry.register(HighCostNodeRule(traverser))
    registry.register(DeepExecutionPlanRule(traverser))

    return ExecutionAnalyzer(registry)