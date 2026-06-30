from __future__ import annotations
from backend.shared.db import get_connection

from backend.execution.contracts.enums import PipelineStatus
from backend.execution.queue.memory_queue import InMemoryQueue
from backend.execution.workers.dispatcher import Dispatcher
from backend.execution.workers.worker import Worker
from backend.execution.workers.worker_pool import WorkerPool

from backend.ingestion.collectors.benchmark_collector import BenchmarkCollector
from backend.ingestion.query_catalog import QueryCatalog
from backend.ingestion.services.ingestion_service import IngestionService

from backend.optimization.pipeline.optimization_pipeline_builder import (
    OptimizationPipelineBuilder,
)
from backend.execution.pipeline.executor import PipelineExecutor

def main() -> None:

    connection = get_connection()

    try:

        pipeline = (
            OptimizationPipelineBuilder(
                connection,
            ).build()
        )

        collector = BenchmarkCollector(
            QueryCatalog(),
        )

        queue = InMemoryQueue()

        executor = PipelineExecutor()

        worker = Worker(queue=queue, executor=executor)

        worker_pool = WorkerPool()

        worker_pool.add_worker(worker)

        dispatcher = Dispatcher(worker_pool.all())

        ingestion = IngestionService(
            collector=collector,
            queue=queue,
            dispatcher=dispatcher,
        )

        results = ingestion.run(pipeline,)

        successful = sum(
            1 for r in results
            if r.status == PipelineStatus.COMPLETED
            )

        failed = len(results) - successful


        print("\n==============================")
        print("Benchmark Summary")
        print("==============================")
        print(f"Total Jobs : {len(results)}")
        print(f"Successful: {successful}")
        print(f"Failed    : {failed}")
        print("==============================")

    finally:
        connection.close()


if __name__ == "__main__":
    main()