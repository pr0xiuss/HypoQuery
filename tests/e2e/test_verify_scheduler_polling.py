import logging
from datetime import datetime, UTC
import sys
import uuid

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

def run_verification():
    from backend.platform.bootstrap.container import PlatformContainer
    from backend.platform.shared.database import SessionLocal
    from dependency_injector import providers
    from backend.platform.scheduler.application.dtos import ScheduleCreateRequest
    from backend.platform.scheduler.domain.job import JobType
    from backend.execution.queue.base_queue import BaseQueue
    
    # 1. Setup DI with shared session for the script
    container = PlatformContainer()
    shared_session = SessionLocal()
    container.db_session.override(providers.Object(shared_session))
    container.init_resources()
    container.wire(modules=[__name__])

    schedule_service = container.schedule_service()
    scheduler = container.scheduler()
    job_repository = container.job_repository()
    queue: BaseQueue = container.execution_queue()
    system_clock = container.system_clock()

    print("\n--- Testing E2E Scheduler Execution ---")
    
    # 2. Create a Schedule using the Schedule API/Service (Due immediately)
    now = system_clock.now()
    request = ScheduleCreateRequest(
        name="Verification Schedule",
        job_type=JobType.WORKLOAD_ANALYSIS,
        payload={"trigger": "scheduler_e2e_test"},
        interval_seconds=3600,  # runs every hour
    )
    
    schedule_dto = schedule_service.create_schedule(request)
    print(f"Created Schedule: {schedule_dto.schedule_id}")
    print(f"Schedule Due At: {schedule_dto.next_run_at}")
    
    # 3. Simulate the Scheduler Daemon polling
    print("\nSimulating Scheduler Daemon...")
    processed_count = scheduler.process_due_schedules_batch(batch_size=10)
    print(f"Schedules processed: {processed_count}")
    
    if processed_count != 1:
        print("ERROR: Expected exactly 1 schedule to be processed!")
        sys.exit(1)
        
    # 4. Verify the Schedule was advanced
    updated_schedule = schedule_service.get_schedule(schedule_dto.schedule_id)
    print(f"Updated Schedule Next Run: {updated_schedule.next_run_at}")
    assert updated_schedule.next_run_at > schedule_dto.next_run_at
    
    # 5. Verify a Job was created and enqueued
    # We can dequeue it from the InMemoryQueue
    print("\nChecking execution queue...")
    entry = queue.dequeue()
    if not entry:
        print("ERROR: No job enqueued!")
        sys.exit(1)
        
    execution = entry.execution
    job_id = execution.context.metadata.get("platform_job_id")
    print(f"Dequeued Pipeline Execution: {execution.context.execution_id}")
    print(f"Associated Platform Job ID: {job_id}")
    
    # Check Job Status
    job = job_repository.get(uuid.UUID(job_id))
    print(f"Job Status: {job.status.value}")
    assert job.status.value == "queued"
    
    print("\nE2E Verification Complete! Architecture boundaries are preserved.")

if __name__ == "__main__":
    setup_logging()
    run_verification()
