from uuid import uuid4

from backend.operations.contracts.snapshots import (
    OptimizationCaseSnapshot,
)
from backend.operations.integration.events.case_events import (
    CaseCreated,
)
from backend.operations.models.enums import (
    CasePriority,
    CaseStatus,
)
from backend.operations.models.identifiers import (
    OptimizationCaseId,
)


def test_case_created_event() -> None:
    snapshot = OptimizationCaseSnapshot(
        case_id=OptimizationCaseId(uuid4()),
        status=CaseStatus.OPEN,
        priority=CasePriority.HIGH,
    )

    event = CaseCreated(
        snapshot=snapshot,
    )

    assert event.snapshot == snapshot