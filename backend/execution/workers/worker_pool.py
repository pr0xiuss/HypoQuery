from __future__ import annotations

from .worker import Worker


class WorkerPool:
    """
    Registry of available workers.
    """

    def __init__(self) -> None:
        self._workers: list[Worker] = []

    def add_worker(self,worker: Worker,) -> None:
        
        self._workers.append(worker)

    def all(self) -> list[Worker]:
        return list(self._workers)

    def size(self) -> int:
        return len(self._workers)