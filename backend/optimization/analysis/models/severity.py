from enum import Enum


class FindingSeverity(str, Enum):
    """
    Represents the importance of an observation.

    Severity describes the observed problem itself.
    It is NOT recommendation priority.
    """

    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"