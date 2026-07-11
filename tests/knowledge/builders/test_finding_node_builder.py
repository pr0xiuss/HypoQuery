from backend.knowledge.models.enums import KnowledgeNodeType
from backend.knowledge.projection.builders.finding_node_builder import (
    FindingNodeBuilder,
)
from backend.optimization.analysis.models.categories import (
    FindingCategory,
)
from backend.optimization.analysis.models.finding import Finding
from backend.optimization.analysis.models.severity import (
    FindingSeverity,
)


def test_build_finding_node() -> None:

    builder = FindingNodeBuilder()

    finding = Finding(
        category=FindingCategory.EXECUTION,
        code="SEQ_SCAN",
        title="Sequential Scan",
        description="Table scan detected.",
        severity=FindingSeverity.HIGH,
    )

    node = builder.build(finding)

    assert node.type == KnowledgeNodeType.FINDING
    assert node.key.value == "finding:SEQ_SCAN"
    assert node.properties["code"] == "SEQ_SCAN"
    assert node.properties["title"] == "Sequential Scan"