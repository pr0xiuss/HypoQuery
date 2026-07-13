from dataclasses import FrozenInstanceError
from uuid import uuid4

import pytest

from backend.operations.cases.models.summary import (
    CaseSummary,
)
from backend.operations.models.enums import (
    CasePriority,
    CaseStatus,
)
from backend.operations.models.identifiers import (
    OptimizationCaseId,
)


def test_case_summary_creation() -> None:
    summary = CaseSummary(
        id=OptimizationCaseId(uuid4()),
        status=CaseStatus.OPEN,
        priority=CasePriority.HIGH,
        total_recommendations=3,
    )

    assert summary.status == CaseStatus.OPEN
    assert summary.priority == CasePriority.HIGH
    assert summary.total_recommendations == 3


def test_case_summary_is_immutable() -> None:
    summary = CaseSummary(
        id=OptimizationCaseId(uuid4()),
        status=CaseStatus.OPEN,
        priority=CasePriority.MEDIUM,
        total_recommendations=1,
    )

    with pytest.raises(FrozenInstanceError):
        summary.priority = CasePriority.CRITICAL