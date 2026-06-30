class QueueError(Exception):
    """Base exception for all queue-related errors."""


class QueueEmptyError(QueueError):
    """Raised when attempting to dequeue from an empty queue."""


class QueueFullError(QueueError):
    """Raised when the queue has reached its capacity."""