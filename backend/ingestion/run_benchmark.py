from __future__ import annotations

from backend.shared.db import get_connection

from backend.execution.bus.in_process_event_bus import InProcessEventBus
from backend.execution.bus.subscriber_registry import SubscriberRegistry
from backend.execution.contracts.enums import PipelineStatus
from backend.execution.events.execution_event_factory import (
    ExecutionEventFactory,
)
from backend.execution.events.execution_event_metadata_provider import (
    ExecutionEventMetadataProvider,
)
from backend.execution.lifecycle.execution_lifecycle import (
    ExecutionLifecycle,
)
from backend.execution.pipeline.executor import PipelineExecutor
from backend.execution.publisher.event_publisher import EventPublisher
from backend.execution.queue.memory_queue import InMemoryQueue
from backend.execution.runtime.execution_runtime import ExecutionRuntime
from backend.execution.runtime.node_runtime import NodeRuntime
from backend.execution.runtime.runtime_context import RuntimeContext
from backend.execution.runtime.system_clock import SystemClock
from backend.execution.workers.dispatcher import Dispatcher
from backend.execution.workers.worker import Worker
from backend.execution.workers.worker_pool import WorkerPool

from backend.ingestion.collectors.benchmark_collector import (
    BenchmarkCollector,
)
from backend.ingestion.query_catalog import QueryCatalog
from backend.ingestion.services.ingestion_service import (
    IngestionService,
)

from backend.optimization.pipeline.optimization_pipeline_builder import (
    OptimizationPipelineBuilder,
)


def main() -> None:
    connection = get_connection()

    try:
        pipeline = OptimizationPipelineBuilder(
            connection,
        ).build()

        collector = BenchmarkCollector(
            QueryCatalog(),
        )

        queue = InMemoryQueue()

        lifecycle = ExecutionLifecycle()

        metadata_provider = ExecutionEventMetadataProvider()

        event_factory = ExecutionEventFactory(
            metadata_provider,
        )

        subscriber_registry = SubscriberRegistry()

        event_bus = InProcessEventBus(
            subscriber_registry,
        )

        publisher = EventPublisher(
            event_bus,
        )

        runtime_context = RuntimeContext(
            lifecycle=lifecycle,
            event_factory=event_factory,
            publisher=publisher,
            clock=SystemClock(),
        )

        runtime = ExecutionRuntime(
            runtime_context,
        )

        node_runtime = NodeRuntime(
            runtime_context,
        )

        executor = PipelineExecutor(
            runtime=runtime,
            node_runtime=node_runtime,
        )

        worker = Worker(
            queue=queue,
            executor=executor,
        )

        worker_pool = WorkerPool()

        worker_pool.add_worker(worker)

        dispatcher = Dispatcher(
            worker_pool.all(),
        )

        ingestion = IngestionService(
            collector=collector,
            queue=queue,
            dispatcher=dispatcher,
        )

        results = ingestion.run(
            pipeline,
        )

        successful = sum(
            1
            for result in results
            if result.status == PipelineStatus.COMPLETED
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