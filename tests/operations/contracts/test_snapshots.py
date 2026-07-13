from dataclasses import FrozenInstanceError
from uuid import uuid4

import pytest

from backend.operations.contracts.snapshots import (
    OptimizationCaseSnapshot,
)
from backend.operations.models.enums import (
    CasePriority,
    CaseStatus,
)
from backend.operations.models.identifiers import (
    OptimizationCaseId,
)


def test_optimization_case_snapshot_creation() -> None:
    snapshot = OptimizationCaseSnapshot(
        case_id=OptimizationCaseId(uuid4()),
        status=CaseStatus.OPEN,
        priority=CasePriority.HIGH,
    )

    assert snapshot.status == CaseStatus.OPEN
    assert snapshot.priority == CasePriority.HIGH


def test_optimization_case_snapshot_is_immutable() -> None:
    snapshot = OptimizationCaseSnapshot(
        case_id=OptimizationCaseId(uuid4()),
        status=CaseStatus.OPEN,
        priority=CasePriority.HIGH,
    )

    with pytest.raises(FrozenInstanceError):
        snapshot.status = CaseStatus.ACTIVE


def test_optimization_case_snapshot_equality() -> None:
    case_id = OptimizationCaseId(uuid4())

    left = OptimizationCaseSnapshot(
        case_id=case_id,
        status=CaseStatus.OPEN,
        priority=CasePriority.MEDIUM,
    )

    right = OptimizationCaseSnapshot(
        case_id=case_id,
        status=CaseStatus.OPEN,
        priority=CasePriority.MEDIUM,
    )

    assert left == right