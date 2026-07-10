from backend.knowledge.models.context_priority import (
    ContextPriority,
)
from backend.knowledge.models.context_section import (
    ContextSection,
)
from backend.knowledge.models.optimization_context import (
    OptimizationContext,
)
from backend.knowledge.models.supporting_evidence import (
    SupportingEvidence,
)
from backend.knowledge.models.node_key import (
    NodeKey,
)
from backend.knowledge.retrieval.evidence.evidence import (
    Evidence,
)
from backend.knowledge.retrieval.evidence.evidence_source import (
    EvidenceSource,
)
from backend.knowledge.retrieval.evidence.evidence_type import (
    EvidenceType,
)


def test_optimization_context():

    context = OptimizationContext()

    context.add_section(
        ContextSection(
            title="Recommendation",
            priority=ContextPriority.PRIMARY,
        )
    )

    context.add_supporting_evidence(
        SupportingEvidence(
            evidence=Evidence(
                key=NodeKey(
                    "recommendation:CREATE_INDEX",
                ),
                type=EvidenceType.RECOMMENDATION,
                source=EvidenceSource.KNOWLEDGE_GRAPH,
            ),
        )
    )

    assert len(
        context.sections,
    ) == 1

    assert len(
        context.supporting_evidence,
    ) == 1