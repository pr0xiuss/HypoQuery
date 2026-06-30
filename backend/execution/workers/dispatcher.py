from __future__ import annotations

from .worker import Worker


class Dispatcher:
    """
    Selects the next available worker.

    Current strategy:
        Round Robin

    Future strategies:
        - Weighted Load Balancing
        - Least Busy
        - Priority Aware
    """

    def __init__(self, workers: list[Worker],) -> None:

        self._workers = workers
        self._current = 0

    def next_worker(self) -> Worker | None:
        """
        Return the next worker according to the dispatch policy.
        """

        if not self._workers:
            return None

        worker = self._workers[self._current]

        self._current = (
            self._current + 1
        ) % len(self._workers)

        return worker