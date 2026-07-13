from backend.operations.models.enums import (
    CaseIntent,
    CasePriority,
    CaseStatus,
)


def test_case_priority_values() -> None:
    assert CasePriority.LOW.value == "low"
    assert CasePriority.MEDIUM.value == "medium"
    assert CasePriority.HIGH.value == "high"
    assert CasePriority.CRITICAL.value == "critical"


def test_case_status_values() -> None:
    assert CaseStatus.OPEN.value == "open"
    assert CaseStatus.ACTIVE.value == "active"
    assert CaseStatus.BLOCKED.value == "blocked"
    assert CaseStatus.COMPLETED.value == "completed"
    assert CaseStatus.ARCHIVED.value == "archived"


def test_case_intent_values() -> None:
    assert CaseIntent.PERFORMANCE.value == "performance"
    assert CaseIntent.STABILITY.value == "stability"
    assert CaseIntent.MAINTENANCE.value == "maintenance"
    assert CaseIntent.COST_REDUCTION.value == "cost_reduction"
    assert (
        CaseIntent.STORAGE_OPTIMIZATION.value
        == "storage_optimization"
    )
    assert (
        CaseIntent.OPERATIONAL_HYGIENE.value
        == "operational_hygiene"
    )