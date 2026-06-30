from __future__ import annotations

from backend.execution.pipeline.pipeline import Pipeline
from backend.execution.queue.base_queue import BaseQueue
from backend.execution.queue.job_record import QueueEntry
from backend.execution.workers.dispatcher import Dispatcher
from backend.ingestion.collectors.base_collector import BaseCollector


class IngestionService:
    """
    Coordinates the ingestion workflow.

    Responsibilities:
        - Collect PipelineExecution objects
        - Enqueue them
        - Dispatch workers to process them
    """

    def __init__(self, collector: BaseCollector, queue: BaseQueue, dispatcher: Dispatcher,) -> None:
        
        self._collector = collector
        self._queue = queue
        self._dispatcher = dispatcher

    def run(self, pipeline: Pipeline,) -> None:
        
        executions = self._collector.collect()

        for execution in executions:
            self._queue.enqueue(
                QueueEntry(
                    execution=execution,
                )
            )

        while not self._queue.is_empty():

            worker = self._dispatcher.next_worker()

            if worker is None:
                break

            worker.process(pipeline)