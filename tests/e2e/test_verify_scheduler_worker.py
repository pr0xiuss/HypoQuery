import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from backend.platform.bootstrap.container import PlatformContainer
from backend.platform.scheduler.application.dtos import JobSubmissionRequest
from backend.platform.scheduler.domain.job import JobType, JobStatus

from backend.execution.pipeline.builder import PipelineBuilder
from backend.execution.pipeline.definition import PipelineDefinition, NodeDefinition
from backend.execution.pipeline.registry import NodeRegistry
from backend.execution.demo.start_node import StartNode
from backend.execution.demo.middle_node import MiddleNode
from backend.execution.demo.end_node import EndNode

from backend.execution.bus.in_process_event_bus import InProcessEventBus
from backend.execution.bus.subscriber_registry import SubscriberRegistry
from backend.execution.events.execution_event_factory import ExecutionEventFactory
from backend.execution.events.execution_event_metadata_provider import ExecutionEventMetadataProvider
from backend.execution.lifecycle.execution_lifecycle import ExecutionLifecycle
from backend.execution.pipeline.executor import PipelineExecutor
from backend.execution.publisher.event_publisher import EventPublisher
from backend.execution.runtime.execution_runtime import ExecutionRuntime
from backend.execution.runtime.node_runtime import NodeRuntime
from backend.execution.runtime.runtime_context import RuntimeContext
from backend.execution.runtime.system_clock import SystemClock
from backend.execution.workers.worker import Worker


def build_test_pipeline():
    registry = NodeRegistry()
    registry.register(StartNode())
    registry.register(MiddleNode())
    registry.register(EndNode())

    definition = PipelineDefinition(
        pipeline_id="demo",
        version="1.0",
        entry_node="start",
        nodes=(
            NodeDefinition("start"),
            NodeDefinition("middle"),
            NodeDefinition("end"),
        ),
        edges={
            "start": ("middle",),
            "middle": ("end",),
            "end": (),
        },
    )
    return PipelineBuilder(registry).build(definition)


def run_verification():
    container = PlatformContainer()
    
    from backend.platform.shared.database import SessionLocal
    from dependency_injector import providers
    shared_session = SessionLocal()
    container.db_session.override(providers.Object(shared_session))
    
    container.init_resources()
    container.wire(modules=[__name__])

    job_service = container.job_service()
    queue = container.execution_queue()
    job_lifecycle_subscriber = container.job_lifecycle_subscriber()
    job_repository = container.job_repository()
    
    # Execution setup
    lifecycle = ExecutionLifecycle()
    metadata_provider = ExecutionEventMetadataProvider()
    event_factory = ExecutionEventFactory(metadata_provider)
    
    subscriber_registry = SubscriberRegistry()
    from backend.execution.contracts.events.pipeline import (
        PipelineStartedEvent,
        PipelineCompletedEvent,
        PipelineFailedEvent,
        PipelineCancelledEvent,
    )
    subscriber_registry.subscribe(PipelineStartedEvent, job_lifecycle_subscriber)
    subscriber_registry.subscribe(PipelineCompletedEvent, job_lifecycle_subscriber)
    subscriber_registry.subscribe(PipelineFailedEvent, job_lifecycle_subscriber)
    subscriber_registry.subscribe(PipelineCancelledEvent, job_lifecycle_subscriber)
    
    event_bus = InProcessEventBus(subscriber_registry)
    publisher = EventPublisher(event_bus)
    
    runtime_context = RuntimeContext(
        lifecycle=lifecycle,
        event_factory=event_factory,
        publisher=publisher,
        clock=SystemClock(),
    )
    
    runtime = ExecutionRuntime(runtime_context)
    node_runtime = NodeRuntime(runtime_context)
    
    executor = PipelineExecutor(
        runtime=runtime,
        node_runtime=node_runtime,
    )
    
    worker = Worker(
        queue=queue,
        executor=executor,
    )
    
    pipeline = build_test_pipeline()
    
    # 1. Submit Job
    print("Submitting job...")
    request = JobSubmissionRequest(
        name="test_e2e_job",
        job_type=JobType.WORKLOAD_ANALYSIS,
        payload={"database": "test_db", "schema": "public"}
    )
    summary = job_service.submit_job(request)
    
    print(f"Job submitted. ID: {summary.job_id}, Status: {summary.status.value}")
    assert summary.status == JobStatus.QUEUED, f"Expected QUEUED, got {summary.status}"
    
    # Get job to check execution ID
    job = job_repository.get(summary.job_id)
    assert job.execution_id is not None
    
    # 2. Worker consumes and processes
    print("Worker processing...")
    result = worker.process(pipeline)
    
    print(f"Worker finished. Pipeline result: {result.status.value if result else 'None'}")
    
    # 3. Verify final state
    updated_job = job_repository.get(summary.job_id)
    print(f"Final Job Status: {updated_job.status.value}")
    assert updated_job.status == JobStatus.COMPLETED, f"Expected COMPLETED, got {updated_job.status}"
    
    # 4. Try failure path
    print("\\nTesting failure path...")
    # Inject a bad pipeline to fail
    request2 = JobSubmissionRequest(
        name="test_e2e_failure",
        job_type=JobType.WORKLOAD_ANALYSIS,
        payload={}
    )
    summary2 = job_service.submit_job(request2)
    print(f"Failure job submitted. ID: {summary2.job_id}")
    
    # process with a None pipeline or fake error? 
    # Let's break the executor or pipeline.
    # Actually, the start node doesn't fail. We can make the worker process with an empty pipeline registry or missing node.
    empty_def = PipelineDefinition(pipeline_id="bad", version="1.0", entry_node="missing", nodes=(), edges={})
    try:
        bad_pipeline = PipelineBuilder(NodeRegistry()).build(empty_def)
        worker.process(bad_pipeline)
    except Exception as e:
        print(f"Pipeline failed as expected (or worker failed).")
        # In this case PipelineExecutor might have failed to even start.
        pass
        
    updated_job2 = job_repository.get(summary2.job_id)
    print(f"Final Failure Job Status: {updated_job2.status.value}")
    
    print("\\nE2E Verification Complete!")

if __name__ == "__main__":
    run_verification()
