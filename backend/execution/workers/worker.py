from __future__ import annotations

from backend.execution.contracts.result import PipelineResult
from backend.execution.pipeline.executor import PipelineExecutor
from backend.execution.pipeline.pipeline import Pipeline
from backend.execution.queue.base_queue import BaseQueue

from .base_worker import BaseWorker


class Worker(BaseWorker):
    """
    Default worker implementation.
    """

    def __init__(self, queue: BaseQueue, executor: PipelineExecutor,) -> None:

        self._queue = queue
        self._executor = executor

    def process(self, pipeline: Pipeline,) -> PipelineResult | None:

        entry = self._queue.dequeue()

        if entry is None:
            return None

        return self._executor.execute(
            pipeline,
            entry.execution,
        )