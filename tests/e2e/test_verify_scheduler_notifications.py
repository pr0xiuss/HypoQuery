import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import logging
import datetime
from uuid import uuid4

from backend.platform.bootstrap.container import PlatformContainer
from backend.platform.scheduler.application.dtos import JobSubmissionRequest
from backend.platform.scheduler.domain.job import JobType, JobStatus
from backend.platform.notifications.domain.notification import NotificationType
from backend.platform.notifications.domain.preference import NotificationPreference

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


logging.basicConfig(level=logging.INFO)


class FailingNode(PipelineNode):
    @property
    def name(self) -> str:
        return "failing_node"
        
    def execute(self, execution) -> NodeResult:
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
    shared_session = SessionLocal()
    
    # Setup test user context
    test_user_id = uuid4()
    
    from dependency_injector import providers
    container.db_session.override(providers.Object(shared_session))
    
    # Clear old data
    from backend.platform.scheduler.infra.job_model import JobModel
    from backend.platform.notifications.infra.notification_model import NotificationModel
    from backend.platform.notifications.infra.preference_model import NotificationPreferenceModel
    
    shared_session.query(JobModel).delete()
    shared_session.query(NotificationModel).delete()
    shared_session.query(NotificationPreferenceModel).delete()
    shared_session.commit()
    
    container.init_resources()
    container.wire(modules=[__name__])

    job_service = container.job_service()
    queue = container.execution_queue()
    job_lifecycle_subscriber = container.job_lifecycle_subscriber()
    notification_subscriber = container.notification_subscriber()
    job_repository = container.job_repository()
    retry_orchestrator = container.retry_orchestrator()
    notification_repo = container.notification_repository()
    pref_repo = container.notification_preference_repository()
    
    # Set explicit preference
    pref = NotificationPreference(
        user_id=test_user_id,
        notification_type=NotificationType.JOB_RETRYING,
        is_enabled=True
    )
    pref_repo.save(pref)
    shared_session.commit()

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
    subscriber_registry.subscribe(PipelineCompletedEvent, notification_subscriber)
    subscriber_registry.subscribe(PipelineFailedEvent, job_lifecycle_subscriber)
    subscriber_registry.subscribe(PipelineFailedEvent, notification_subscriber)
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
    
    print("--- 1. Submitting Job with User ID ---")
    request = JobSubmissionRequest(
        name="test_notification_job",
        job_type=JobType.WORKLOAD_ANALYSIS,
        payload={"database": "test_db", "schema": "public", "user_id": str(test_user_id)}
    )
    summary = job_service.submit_job(request)
    job_id = summary.job_id
    
    print(f"\\n--- Attempt 1 ---")
    worker.process(pipeline)
    job = job_repository.get(job_id)
    assert job.status == JobStatus.PENDING_RETRY
    assert job.attempt_count == 1
    
    # Verify Notification
    notifications = notification_repo.list_for_user(test_user_id)
    assert len(notifications) == 1
    assert notifications[0].notification_type == NotificationType.JOB_RETRYING
    assert notifications[0].execution_id == job.execution_id
    print(f"Success: Received JOB_RETRYING notification for Attempt 1. Title: {notifications[0].title}")
    
    # Try idempotent duplicate process (should not create another notification)
    print(f"\\n--- Attempt 1 (Idempotency check) ---")
    
    # We fake an event payload directly to trigger the subscriber again
    from backend.execution.contracts.events.pipeline import PipelineFailedEvent
    from backend.execution.contracts.events.base import EventMetadata
    
    dummy_event = PipelineFailedEvent(
        error="Simulated transient connection failure",
        error_type="ConnectionError",
        metadata=EventMetadata(
            event_id=uuid4(),
            trace_id=job.execution_id,
            sequence_number=2,
            event_version="1.0",
            timestamp=datetime.datetime.now(datetime.UTC),
            execution_id=job.execution_id,
            metadata={
                "platform_job_id": str(job.job_id),
                "job_attempt_count": 1,
                "job_max_attempts": 3,
            }
        )
    )
    
    notification_subscriber.handle(dummy_event)
    notifications_after = notification_repo.list_for_user(test_user_id)
    assert len(notifications_after) == 1
    print("Success: Idempotency check passed (no duplicate notification created).")

    # Fast forward time
    job = job.with_retry_tracking(
        attempt_count=job.attempt_count,
        last_attempt_at=job.last_attempt_at,
        next_attempt_at=datetime.datetime.now(datetime.UTC)
    )
    job_repository.save(job)
    shared_session.commit()
    
    # Trigger retry orchestrator
    retry_orchestrator.process_due_retries()
    
    print(f"\\n--- Attempt 2 ---")
    worker.process(pipeline)
    job = job_repository.get(job_id)
    assert job.status == JobStatus.PENDING_RETRY
    
    notifications = notification_repo.list_for_user(test_user_id)
    assert len(notifications) == 2
    # The newest one should be first
    assert notifications[0].notification_type == NotificationType.JOB_RETRYING
    assert notifications[0].execution_id == job.execution_id
    print(f"Success: Received second JOB_RETRYING notification for Attempt 2.")

    # Fast forward time
    job = job.with_retry_tracking(
        attempt_count=job.attempt_count,
        last_attempt_at=job.last_attempt_at,
        next_attempt_at=datetime.datetime.now(datetime.UTC)
    )
    job_repository.save(job)
    shared_session.commit()
    retry_orchestrator.process_due_retries()
    
    print(f"\\n--- Attempt 3 (Final Failure) ---")
    worker.process(pipeline)
    job = job_repository.get(job_id)
    assert job.status == JobStatus.FAILED
    
    notifications = notification_repo.list_for_user(test_user_id)
    assert len(notifications) == 3
    assert notifications[0].notification_type == NotificationType.JOB_FAILED
    assert notifications[0].execution_id == job.execution_id
    print(f"Success: Received JOB_FAILED notification for Attempt 3. Title: {notifications[0].title}")

    print("\\nE2E Notification Verification Complete!")

if __name__ == "__main__":
    run_verification()
