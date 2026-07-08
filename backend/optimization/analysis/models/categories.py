from enum import Enum


class FindingCategory(str, Enum):
    """High-level categories used to classify analysis findings."""

    EXECUTION = "execution"
    HEALTH = "health"
    CONFIGURATION = "configuration"
    WORKLOAD = "workload"