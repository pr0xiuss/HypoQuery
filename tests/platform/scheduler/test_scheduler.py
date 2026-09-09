import pytest
from datetime import datetime, UTC, timedelta
from unittest.mock import Mock, call
from uuid import uuid4

from backend.platform.scheduler.application.scheduler import Scheduler
from backend.platform.scheduler.application.schedule_calculator import ScheduleCalculator
from backend.platform.scheduler.domain.schedule import Schedule
from backend.platform.scheduler.domain.job import JobType


def test_scheduler_process_due_schedules():
    repo = Mock()
    job_service = Mock()
    transaction_manager = Mock()
    clock = Mock()
    clock.now.return_value = datetime(2025, 1, 1, 12, 0, 0, tzinfo=UTC)
    calc = ScheduleCalculator(clock)

    scheduler = Scheduler(
        schedule_repository=repo,
        job_service=job_service,
        schedule_calculator=calc,
        transaction_manager=transaction_manager,
    )

    # Setup 1 due schedule
    sched = Schedule(
        schedule_id=uuid4(),
        name="Test",
        job_type=JobType.WORKLOAD_ANALYSIS,
        payload={},
        interval_seconds=3600,
        is_enabled=True,
        next_run_at=datetime(2025, 1, 1, 11, 0, 0, tzinfo=UTC),
    )
    
    # First call returns 1 schedule, second returns empty to break the loop
    repo.get_due_schedules.side_effect = [[sched], []]

    processed = scheduler.process_due_schedules_batch(batch_size=10)

    assert processed == 1
    assert repo.get_due_schedules.call_count == 2
    
    # Advanced schedule should be saved
    assert repo.save.call_count == 1
    saved_sched = repo.save.call_args[0][0]
    assert saved_sched.next_run_at == datetime(2025, 1, 1, 13, 0, 0, tzinfo=UTC)
    
    # Job should be submitted
    assert job_service.submit_job.call_count == 1
    req = job_service.submit_job.call_args[0][0]
    assert req.name == "Test - Scheduled Run"
    assert req.job_type == JobType.WORKLOAD_ANALYSIS

    # Since JobService manages its own commit, transaction_manager.commit is not called here
    assert transaction_manager.commit.call_count == 0


def test_scheduler_handles_job_submission_failure():
    repo = Mock()
    job_service = Mock()
    transaction_manager = Mock()
    clock = Mock()
    clock.now.return_value = datetime(2025, 1, 1, 12, 0, 0, tzinfo=UTC)
    calc = ScheduleCalculator(clock)

    scheduler = Scheduler(
        schedule_repository=repo,
        job_service=job_service,
        schedule_calculator=calc,
        transaction_manager=transaction_manager,
    )

    sched = Schedule(
        schedule_id=uuid4(),
        name="Test",
        job_type=JobType.WORKLOAD_ANALYSIS,
        payload={},
        interval_seconds=3600,
        is_enabled=True,
        next_run_at=datetime(2025, 1, 1, 11, 0, 0, tzinfo=UTC),
    )
    repo.get_due_schedules.return_value = [sched]
    
    # Simulate job service raising an exception
    job_service.submit_job.side_effect = Exception("DB error")

    # Only run 1 iteration
    scheduler.process_next_due_schedule()

    # The transaction should be rolled back!
    assert transaction_manager.rollback.call_count == 1
    assert transaction_manager.commit.call_count == 0
