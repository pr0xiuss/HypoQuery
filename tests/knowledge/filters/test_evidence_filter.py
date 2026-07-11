from backend.knowledge.filters.evidence_filter import (
    EvidenceFilter,
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


def test_evidence_filter():

    recommendation = Evidence(
        key=NodeKey(
            "recommendation:CREATE_INDEX",
        ),
        type=EvidenceType.RECOMMENDATION,
        source=EvidenceSource.KNOWLEDGE_GRAPH,
    )

    finding = Evidence(
        key=NodeKey(
            "finding:SEQ_SCAN",
        ),
        type=EvidenceType.FINDING,
        source=EvidenceSource.KNOWLEDGE_GRAPH,
    )

    filtered = EvidenceFilter().by_type(
        (
            recommendation,
            finding,
        ),
        EvidenceType.RECOMMENDATION,
    )

    assert len(
        filtered,
    ) == 1

    assert (
        filtered[0].type
        == EvidenceType.RECOMMENDATION
    )