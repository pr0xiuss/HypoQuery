from dataclasses import FrozenInstanceError

import pytest

from backend.operations.cases.models.metadata import (
    CaseMetadata,
)
from backend.operations.models.enums import (
    CaseIntent,
)


def test_case_metadata_creation() -> None:
    metadata = CaseMetadata(
        intent=CaseIntent.PERFORMANCE,
    )

    assert metadata.intent == CaseIntent.PERFORMANCE
    assert metadata.labels == []


def test_case_metadata_is_immutable() -> None:
    metadata = CaseMetadata(
        intent=CaseIntent.STABILITY,
    )

    with pytest.raises(FrozenInstanceError):
        metadata.intent = CaseIntent.MAINTENANCE


def test_case_metadata_default_labels() -> None:
    metadata = CaseMetadata(
        intent=CaseIntent.OPERATIONAL_HYGIENE,
    )

    assert len(metadata.labels) == 0