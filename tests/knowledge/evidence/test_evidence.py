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


def test_evidence():

    evidence = Evidence(
        key=NodeKey(
            "recommendation:CREATE_INDEX",
        ),
        type=EvidenceType.RECOMMENDATION,
        source=EvidenceSource.KNOWLEDGE_GRAPH,
        confidence=0.95,
    )

    assert evidence.key.value == (
        "recommendation:CREATE_INDEX"
    )

    assert (
        evidence.type
        == EvidenceType.RECOMMENDATION
    )

    assert (
        evidence.source
        == EvidenceSource.KNOWLEDGE_GRAPH
    )

    assert evidence.confidence == 0.95