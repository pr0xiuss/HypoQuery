from backend.knowledge.models.node_key import (
    NodeKey,
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


def build_evidence(
    key: str,
    confidence: float,
) -> Evidence:

    return Evidence(
        key=NodeKey(
            key,
        ),
        type=EvidenceType.RECOMMENDATION,
        source=EvidenceSource.KNOWLEDGE_GRAPH,
        confidence=confidence,
    )


def test_evidence_set():

    evidence = EvidenceSet()

    first = build_evidence(
        "a",
        0.5,
    )

    second = build_evidence(
        "b",
        1.0,
    )

    evidence.add(
        first,
    )

    evidence.add(
        second,
    )

    assert len(
        evidence,
    ) == 2

    assert evidence.contains(
        NodeKey("a"),
    )

    evidence.sort()

    assert (
        evidence.items[0]
        == second
    )

    evidence.deduplicate()

    assert len(
        evidence,
    ) == 2