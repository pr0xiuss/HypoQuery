from collections import deque

from .base_queue import BaseQueue
from .job_record import QueueEntry


class InMemoryQueue(BaseQueue):
    """
    Simple FIFO queue used for testing and local execution.
    """

    def __init__(self) -> None:
        self._queue: deque[QueueEntry] = deque()

    def enqueue(self, entry: QueueEntry) -> None:
        self._queue.append(entry)

    def dequeue(self) -> QueueEntry:

        if self.is_empty():
            return None

        return self._queue.popleft()

    def peek(self) -> QueueEntry:

        if self.is_empty():
            return None

        return self._queue[0]

    def is_empty(self) -> bool:
        return len(self._queue) == 0

    def size(self) -> int:
        return len(self._queue)