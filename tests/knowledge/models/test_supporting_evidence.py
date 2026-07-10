from backend.knowledge.models.node_key import (
    NodeKey,
)
from backend.knowledge.models.supporting_evidence import (
    SupportingEvidence,
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


def test_supporting_evidence():

    supporting = SupportingEvidence(
        evidence=Evidence(
            key=NodeKey(
                "recommendation:CREATE_INDEX",
            ),
            type=EvidenceType.RECOMMENDATION,
            source=EvidenceSource.KNOWLEDGE_GRAPH,
        ),
        explanation="Validated recommendation",
    )

    assert (
        supporting.evidence.key.value
        == "recommendation:CREATE_INDEX"
    )

    assert (
        supporting.explanation
        == "Validated recommendation"
    )