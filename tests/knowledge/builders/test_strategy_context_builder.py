from backend.knowledge.builders.strategy_context_builder import (
    StrategyContextBuilder,
)
from backend.knowledge.context import ContextContext
from backend.knowledge.context_state.job import (
    ContextJob,
)
from backend.knowledge.models.context_priority import (
    ContextPriority,
)
from backend.knowledge.models.node_key import (
    NodeKey,
)
from backend.knowledge.models.optimization_context import (
    OptimizationContext,
)
from backend.knowledge.retrieval.evidence.evidence import (
    Evidence,
)
from backend.knowledge.retrieval.evidence.evidence_set import (
    EvidenceSet,
)
from backend.knowledge.retrieval.evidence.evidence_source import (
    EvidenceSource,
)
from backend.knowledge.retrieval.evidence.evidence_type import (
    EvidenceType,
)
from backend.knowledge.retrieval.objectives.objective_type import (
    ObjectiveType,
)
from backend.knowledge.retrieval.objectives.retrieval_objective import (
    RetrievalObjective,
)


def test_strategy_context_builder():

    evidence = EvidenceSet()

    evidence.add(
        Evidence(
            key=NodeKey(
                "strategy:INDEXING",
            ),
            type=EvidenceType.STRATEGY,
            source=EvidenceSource.KNOWLEDGE_GRAPH,
        )
    )

    context = ContextContext(
        job=ContextJob(
            objective=RetrievalObjective(
                type=ObjectiveType.FIND_STRATEGIES,
            ),
            evidence=evidence,
        ),
    )

    optimization_context = OptimizationContext()

    StrategyContextBuilder().build(
        context,
        optimization_context,
    )

    assert len(
        optimization_context.sections,
    ) == 1

    assert (
        optimization_context.sections[0].priority
        == ContextPriority.SUPPORTING
    )