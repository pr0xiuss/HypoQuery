from unittest.mock import Mock, MagicMock
from uuid import uuid4
from datetime import datetime, timezone

from backend.platform.scheduler.application.retry_orchestrator import RetryOrchestrator
from backend.platform.scheduler.domain.job import Job, JobType, JobStatus
from backend.execution.runtime.system_clock import SystemClock


def test_retry_orchestrator_processes_due_jobs():
    job_repository = Mock()
    job_service = Mock()
    clock = Mock(spec=SystemClock)
    transaction_manager = MagicMock()
    
    now = datetime.now(timezone.utc)
    clock.now.return_value = now

    job = Job(
        name="test",
        job_type=JobType.WORKLOAD_ANALYSIS,
        payload={},
        status=JobStatus.PENDING_RETRY,
        attempt_count=1,
        max_attempts=3,
        next_attempt_at=now
    )
    
    # Return 1 job on first call, then empty on second call
    job_repository.get_jobs_due_for_retry.side_effect = [[job], []]
    
    orchestrator = RetryOrchestrator(
        job_repository=job_repository,
        job_service=job_service,
        clock=clock,
        transaction_manager=transaction_manager
    )
    
    processed = orchestrator.process_due_retries(batch_size=10)
    
    assert processed == 1
    job_service.retry_job.assert_called_once_with(job.job_id)
    # The orchestrator should not commit manually, but instead job_service handles commit.
    # However in our implementation it does not call commit directly on transaction_manager. Wait, does it?
    # Actually _process_next_due_retry doesn't call commit, job_service does.
    # So we just verify job_service.retry_job was called.

def test_retry_orchestrator_stops_on_empty():
    job_repository = Mock()
    job_service = Mock()
    clock = Mock(spec=SystemClock)
    transaction_manager = MagicMock()
    
    now = datetime.now(timezone.utc)
    clock.now.return_value = now
    
    job_repository.get_jobs_due_for_retry.return_value = []
    
    orchestrator = RetryOrchestrator(
        job_repository=job_repository,
        job_service=job_service,
        clock=clock,
        transaction_manager=transaction_manager
    )
    
    processed = orchestrator.process_due_retries(batch_size=10)
    
    assert processed == 0
    job_service.retry_job.assert_not_called()
