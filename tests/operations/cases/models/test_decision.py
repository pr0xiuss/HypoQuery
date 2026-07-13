from dataclasses import FrozenInstanceError

import pytest

from backend.operations.cases.models.decision import (
    Decision,
)


def test_decision_creation() -> None:
    decision = Decision(
        action="accept",
        actor="DBA",
        reason="Improves query performance.",
    )

    assert decision.action == "accept"
    assert decision.actor == "DBA"
    assert decision.reason == "Improves query performance."


def test_decision_is_immutable() -> None:
    decision = Decision(
        action="reject",
        actor="Engineer",
    )

    with pytest.raises(FrozenInstanceError):
        decision.action = "accept"


def test_decision_reason_defaults_to_none() -> None:
    decision = Decision(
        action="archive",
        actor="System",
    )

    assert decision.reason is None