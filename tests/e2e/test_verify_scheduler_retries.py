import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from backend.platform.bootstrap.container import PlatformContainer
from backend.platform.scheduler.application.dtos import JobSubmissionRequest
from backend.platform.scheduler.domain.job import JobType, JobStatus

from backend.execution.pipeline.builder import PipelineBuilder
from backend.execution.pipeline.definition import PipelineDefinition, NodeDefinition
from backend.execution.pipeline.registry import NodeRegistry
from backend.execution.pipeline.base_node import PipelineNode
from backend.execution.contracts.node_result import NodeResult
from backend.execution.contracts.enums import NodeStatus

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


class FailingNode(PipelineNode):
    @property
    def name(self) -> str:
        return "failing_node"
        
    def execute(self, execution) -> NodeResult:
        # Throw a retryable exception
        raise ConnectionError("Simulated transient connection failure")
        

def build_failing_pipeline():
    registry = NodeRegistry()
    registry.register(FailingNode())

    definition = PipelineDefinition(
        pipeline_id="demo_fail",
        version="1.0",
        entry_node="failing_node",
        nodes=(
            NodeDefinition("failing_node"),
        ),
        edges={
            "failing_node": (),
        },
    )
    return PipelineBuilder(registry).build(definition)


def run_verification():
    container = PlatformContainer()
    
    from backend.platform.shared.database import SessionLocal
    from dependency_injector import providers
    shared_session = SessionLocal()
    container.db_session.override(providers.Object(shared_session))
    
    # Clear old jobs
    from backend.platform.scheduler.infra.job_model import JobModel
    shared_session.query(JobModel).delete()
    shared_session.commit()
    
    container.init_resources()
    container.wire(modules=[__name__])

    job_service = container.job_service()
    queue = container.execution_queue()
    job_lifecycle_subscriber = container.job_lifecycle_subscriber()
    job_repository = container.job_repository()
    retry_orchestrator = container.retry_orchestrator()
    
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
    
    pipeline = build_failing_pipeline()
    
    # 1. Submit Job
    print("Submitting job...")
    request = JobSubmissionRequest(
        name="test_retry_job",
        job_type=JobType.WORKLOAD_ANALYSIS,
        payload={"database": "test_db", "schema": "public"}
    )
    summary = job_service.submit_job(request)
    
    print(f"Job submitted. ID: {summary.job_id}")
    
    job_id = summary.job_id
    
    # ATTEMPT 1
    print("\\n--- Attempt 1 ---")
    worker.process(pipeline)
    job = job_repository.get(job_id)
    print(f"Status after attempt 1: {job.status.value}, Attempts: {job.attempt_count}")
    assert job.status == JobStatus.PENDING_RETRY
    assert job.attempt_count == 1
    
    # Force next_attempt_at to now for testing
    import datetime
    job = job.with_retry_tracking(
        attempt_count=job.attempt_count,
        last_attempt_at=job.last_attempt_at,
        next_attempt_at=datetime.datetime.now(datetime.UTC)
    )
    job_repository.save(job)
    shared_session.commit()
    
    # Trigger retry orchestrator
    processed = retry_orchestrator.process_due_retries()
    print(f"Retry orchestrator processed {processed} jobs.")
    job = job_repository.get(job_id)
    print(f"Status after orchestrator: {job.status.value}")
    assert job.status == JobStatus.QUEUED
    
    # ATTEMPT 2
    print("\\n--- Attempt 2 ---")
    worker.process(pipeline)
    job = job_repository.get(job_id)
    print(f"Status after attempt 2: {job.status.value}, Attempts: {job.attempt_count}")
    assert job.status == JobStatus.PENDING_RETRY
    assert job.attempt_count == 2
    
    # Force next_attempt_at to now for testing
    job = job.with_retry_tracking(
        attempt_count=job.attempt_count,
        last_attempt_at=job.last_attempt_at,
        next_attempt_at=datetime.datetime.now(datetime.UTC)
    )
    job_repository.save(job)
    shared_session.commit()
    
    # Trigger retry orchestrator
    processed = retry_orchestrator.process_due_retries()
    print(f"Retry orchestrator processed {processed} jobs.")
    job = job_repository.get(job_id)
    assert job.status == JobStatus.QUEUED
    
    # ATTEMPT 3
    print("\\n--- Attempt 3 ---")
    worker.process(pipeline)
    job = job_repository.get(job_id)
    print(f"Status after attempt 3: {job.status.value}, Attempts: {job.attempt_count}")
    # Since max_attempts=3, after attempt 3 fails, it should be FAILED.
    assert job.status == JobStatus.FAILED
    assert job.attempt_count == 3
    
    print("\\nE2E Retry Verification Complete!")

if __name__ == "__main__":
    run_verification()
