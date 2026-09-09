import sys
from pathlib import Path
import logging
import datetime
import threading
from uuid import uuid4

sys.path.append(str(Path(__file__).parent.parent))

from backend.platform.bootstrap.container import PlatformContainer
from backend.platform.scheduler.application.dtos import JobSubmissionRequest
from backend.platform.scheduler.domain.job import JobType, JobStatus
from backend.platform.scheduler.domain.schedule import Schedule
from backend.platform.notifications.domain.notification import NotificationType
from backend.platform.notifications.domain.preference import NotificationPreference

from backend.execution.pipeline.builder import PipelineBuilder
from backend.execution.pipeline.definition import PipelineDefinition, NodeDefinition
from backend.execution.pipeline.registry import NodeRegistry
from backend.execution.pipeline.base_node import PipelineNode
from backend.execution.contracts.node_result import NodeResult

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

class SucceedingNode(PipelineNode):
    @property
    def name(self) -> str:
        return "succeeding_node"
        
    def execute(self, execution) -> NodeResult:
        return NodeResult.success()

class FailingNode(PipelineNode):
    @property
    def name(self) -> str:
        return "failing_node"
        
    def execute(self, execution) -> NodeResult:
        raise ConnectionError("Simulated transient connection failure")

def build_pipeline(node_cls, entry_name: str, pipeline_id: str):
    registry = NodeRegistry()
    registry.register(node_cls())

    definition = PipelineDefinition(
        pipeline_id=pipeline_id,
        version="1.0",
        entry_node=entry_name,
        nodes=(NodeDefinition(entry_name),),
        edges={entry_name: ()},
    )
    return PipelineBuilder(registry).build(definition)

def create_scheduler(container, shared_session):
    from backend.platform.scheduler.application.scheduler import Scheduler
    from backend.platform.scheduler.application.job_service import JobService
    from backend.platform.scheduler.application.schedule_calculator import ScheduleCalculator
    from backend.platform.scheduler.infra.sqlalchemy_schedule_repo import SqlAlchemyScheduleRepository
    from backend.platform.scheduler.infra.sqlalchemy_job_repo import SqlAlchemyJobRepository
    from backend.execution.queue.memory_queue import InMemoryQueue
    from backend.platform.shared.transactions.sqlalchemy_transaction_manager import SQLAlchemyTransactionManager

    # Need a fresh session for concurrent tests
    from backend.platform.shared.database import SessionLocal
    sess = SessionLocal()
    tm = SQLAlchemyTransactionManager(sess)
    schedule_repo = SqlAlchemyScheduleRepository(sess)
    job_repo = SqlAlchemyJobRepository(sess)
    queue = InMemoryQueue()
    job_svc = JobService(job_repository=job_repo, transaction_manager=tm, queue=queue)
    calc = ScheduleCalculator(SystemClock())
    return Scheduler(schedule_repo, job_svc, calc, tm), sess

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
    from backend.platform.scheduler.infra.schedule_model import ScheduleModel
    from backend.platform.notifications.infra.notification_model import NotificationModel
    from backend.platform.notifications.infra.preference_model import NotificationPreferenceModel
    
    shared_session.query(JobModel).delete()
    shared_session.query(ScheduleModel).delete()
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
    schedule_repo = container.schedule_repository()
    
    # Enable all relevant preferences
    for n_type in [NotificationType.JOB_RETRYING, NotificationType.JOB_FAILED, NotificationType.JOB_COMPLETED]:
        pref_repo.save(NotificationPreference(user_id=test_user_id, notification_type=n_type, is_enabled=True))
    shared_session.commit()

    # Execution setup
    lifecycle = ExecutionLifecycle()
    metadata_provider = ExecutionEventMetadataProvider()
    event_factory = ExecutionEventFactory(metadata_provider)
    
    subscriber_registry = SubscriberRegistry()
    from backend.execution.contracts.events.pipeline import (
        PipelineStartedEvent, PipelineCompletedEvent, PipelineFailedEvent, PipelineCancelledEvent
    )
    subscriber_registry.subscribe(PipelineStartedEvent, job_lifecycle_subscriber)
    subscriber_registry.subscribe(PipelineCompletedEvent, job_lifecycle_subscriber)
    subscriber_registry.subscribe(PipelineCompletedEvent, notification_subscriber)
    subscriber_registry.subscribe(PipelineFailedEvent, job_lifecycle_subscriber)
    subscriber_registry.subscribe(PipelineFailedEvent, notification_subscriber)
    subscriber_registry.subscribe(PipelineCancelledEvent, job_lifecycle_subscriber)
    
    event_bus = InProcessEventBus(subscriber_registry)
    publisher = EventPublisher(event_bus)
    
    runtime_context = RuntimeContext(lifecycle=lifecycle, event_factory=event_factory, publisher=publisher, clock=SystemClock())
    runtime = ExecutionRuntime(runtime_context)
    node_runtime = NodeRuntime(runtime_context)
    executor = PipelineExecutor(runtime=runtime, node_runtime=node_runtime)
    worker = Worker(queue=queue, executor=executor)
    
    failing_pipeline = build_pipeline(FailingNode, "failing_node", "demo_fail")
    succeeding_pipeline = build_pipeline(SucceedingNode, "succeeding_node", "demo_success")
    
    print("\\n===========================================")
    print("SCENARIO A: SUCCESS")
    print("===========================================")
    request = JobSubmissionRequest(
        name="test_success_job",
        job_type=JobType.WORKLOAD_ANALYSIS,
        payload={"database": "test_db", "schema": "public", "user_id": str(test_user_id)}
    )
    summary = job_service.submit_job(request)
    job_id = summary.job_id
    
    worker.process(succeeding_pipeline)
    job = job_repository.get(job_id)
    assert job.status == JobStatus.COMPLETED
    
    notifications = notification_repo.list_for_user(test_user_id)
    comp_notifs = [n for n in notifications if n.job_id == job_id]
    assert len(comp_notifs) == 1
    assert comp_notifs[0].notification_type == NotificationType.JOB_COMPLETED
    print("Success: Scenario A verified (COMPLETED Job + Notification).")

    print("\\n===========================================")
    print("SCENARIO B & C: RETRY & EXHAUSTION")
    print("===========================================")
    request = JobSubmissionRequest(
        name="test_failing_job",
        job_type=JobType.WORKLOAD_ANALYSIS,
        payload={"database": "test_db", "schema": "public", "user_id": str(test_user_id)}
    )
    summary = job_service.submit_job(request)
    job_id = summary.job_id
    
    print("--- Attempt 1 ---")
    worker.process(failing_pipeline)
    job = job_repository.get(job_id)
    assert job.status == JobStatus.PENDING_RETRY
    assert job.attempt_count == 1
    
    notifications = notification_repo.list_for_user(test_user_id)
    retry_notifs = [n for n in notifications if n.job_id == job_id]
    assert len(retry_notifs) == 1
    assert retry_notifs[0].notification_type == NotificationType.JOB_RETRYING
    
    print("--- Attempt 2 ---")
    # fast forward
    job = job.with_retry_tracking(attempt_count=job.attempt_count, last_attempt_at=job.last_attempt_at, next_attempt_at=datetime.datetime.now(datetime.UTC))
    job_repository.save(job)
    shared_session.commit()
    retry_orchestrator.process_due_retries()
    worker.process(failing_pipeline)
    job = job_repository.get(job_id)
    assert job.status == JobStatus.PENDING_RETRY
    
    notifications = notification_repo.list_for_user(test_user_id)
    retry_notifs = [n for n in notifications if n.job_id == job_id and n.notification_type == NotificationType.JOB_RETRYING]
    assert len(retry_notifs) == 2
    
    print("--- Attempt 3 (Final) ---")
    job = job.with_retry_tracking(attempt_count=job.attempt_count, last_attempt_at=job.last_attempt_at, next_attempt_at=datetime.datetime.now(datetime.UTC))
    job_repository.save(job)
    shared_session.commit()
    retry_orchestrator.process_due_retries()
    worker.process(failing_pipeline)
    job = job_repository.get(job_id)
    assert job.status == JobStatus.FAILED
    
    notifications = notification_repo.list_for_user(test_user_id)
    fail_notifs = [n for n in notifications if n.job_id == job_id and n.notification_type == NotificationType.JOB_FAILED]
    assert len(fail_notifs) == 1
    print("Success: Scenario B & C verified (PENDING_RETRY + Exhaustion FAILED with notifications).")

    print("\\n===========================================")
    print("SCENARIO D: IDEMPOTENCY")
    print("===========================================")
    from backend.execution.contracts.events.pipeline import PipelineFailedEvent
    from backend.execution.contracts.events.base import EventMetadata
    dummy_event = PipelineFailedEvent(
        error="Simulated transient connection failure", error_type="ConnectionError",
        metadata=EventMetadata(event_id=uuid4(), trace_id=job.execution_id, sequence_number=4, event_version="1.0",
                               timestamp=datetime.datetime.now(datetime.UTC), execution_id=job.execution_id,
                               metadata={"platform_job_id": str(job.job_id), "job_attempt_count": 3, "job_max_attempts": 3})
    )
    notification_subscriber.handle(dummy_event)
    notifications = notification_repo.list_for_user(test_user_id)
    fail_notifs_after = [n for n in notifications if n.job_id == job_id and n.notification_type == NotificationType.JOB_FAILED]
    assert len(fail_notifs_after) == 1
    print("Success: Scenario D verified (Idempotent Notification Handling).")

    print("\\n===========================================")
    print("SCENARIO E: PREFERENCES")
    print("===========================================")
    pref = pref_repo.get_by_user_and_type(test_user_id, NotificationType.JOB_COMPLETED)
    pref_repo.save(pref.with_status(is_enabled=False))
    shared_session.commit()
    
    request = JobSubmissionRequest(name="test_suppressed_job", job_type=JobType.WORKLOAD_ANALYSIS, payload={"database": "test_db", "schema": "public", "user_id": str(test_user_id)})
    summary = job_service.submit_job(request)
    worker.process(succeeding_pipeline)
    
    notifications = notification_repo.list_for_user(test_user_id)
    suppressed = [n for n in notifications if n.job_id == summary.job_id]
    assert len(suppressed) == 0
    print("Success: Scenario E verified (Notification suppressed when preference is OFF).")

    print("\\n===========================================")
    print("SCENARIO F: CONCURRENCY")
    print("===========================================")
    now = datetime.datetime.now(datetime.UTC)
    s = Schedule(schedule_id=uuid4(), name="Concurrency Test", job_type=JobType.WORKLOAD_ANALYSIS, payload={"user_id": str(test_user_id)},
                 interval_seconds=60, is_enabled=True, next_run_at=now - datetime.timedelta(minutes=1))
    schedule_repo.save(s)
    shared_session.commit()

    s1, sess1 = create_scheduler(container, shared_session)
    s2, sess2 = create_scheduler(container, shared_session)

    processed_counts = [0, 0]
    
    def run_s1():
        processed_counts[0] = s1.process_due_schedules_batch(batch_size=5)
        sess1.close()

    def run_s2():
        processed_counts[1] = s2.process_due_schedules_batch(batch_size=5)
        sess2.close()

    t1 = threading.Thread(target=run_s1)
    t2 = threading.Thread(target=run_s2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    total_processed = processed_counts[0] + processed_counts[1]
    assert total_processed == 1, f"Expected exactly 1 schedule to be processed, got {total_processed}"
    
    jobs, count = job_repository.list_jobs(limit=10)
    concurrency_jobs = [j for j in jobs if j.name == "Concurrency Test - Scheduled Run"]
    assert len(concurrency_jobs) == 1, f"Expected exactly 1 job to be created, got {len(concurrency_jobs)}"
    print("Success: Scenario F verified (FOR UPDATE SKIP LOCKED protected concurrent execution).")

    print("\\n===========================================")
    print("✅ FULL MODULE 6 VERIFICATION COMPLETE")
    print("===========================================")

if __name__ == "__main__":
    run_verification()
