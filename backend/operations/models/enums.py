from __future__ import annotations

from enum import Enum


class CasePriority(str, Enum):
    """
    Priority assigned to an Optimization Case.
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class CaseStatus(str, Enum):
    """
    Current lifecycle state of an Optimization Case.

    NOTE:
    The lifecycle itself is event-driven.
    This status represents the current operational view.
    """

    OPEN = "open"
    ACTIVE = "active"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class CaseIntent(str, Enum):
    """
    Primary engineering objective of an Optimization Case.
    """

    PERFORMANCE = "performance"
    STABILITY = "stability"
    MAINTENANCE = "maintenance"
    COST_REDUCTION = "cost_reduction"
    STORAGE_OPTIMIZATION = "storage_optimization"
    OPERATIONAL_HYGIENE = "operational_hygiene"