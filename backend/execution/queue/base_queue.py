from __future__ import annotations

from abc import ABC, abstractmethod

from .job_record import QueueEntry


class BaseQueue(ABC):
    """
    Abstract queue interface.

    All queue implementations (memory, Redis, etc.)
    must implement this contract.
    """

    @abstractmethod
    def enqueue(self, job: QueueEntry) -> None:
        raise NotImplementedError

    @abstractmethod
    def dequeue(self) -> QueueEntry | None:
        raise NotImplementedError

    @abstractmethod
    def peek(self) -> QueueEntry | None:
        raise NotImplementedError

    @abstractmethod
    def is_empty(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def size(self) -> int:
        raise NotImplementedError