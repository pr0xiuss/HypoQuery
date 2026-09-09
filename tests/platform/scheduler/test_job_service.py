import pytest
from unittest.mock import Mock, MagicMock
from uuid import uuid4

from backend.execution.queue.base_queue import BaseQueue
from backend.execution.queue.job_record import QueueEntry
from backend.platform.scheduler.application.job_service import JobService, JobNotFoundError
from backend.platform.scheduler.application.dtos import JobSubmissionRequest
from backend.platform.scheduler.domain.job import Job, JobStatus, JobType
from backend.platform.scheduler.repositories.job_repository import JobRepository
from backend.platform.shared.transactions.transaction_manager import TransactionManager


@pytest.fixture
def mock_transaction_manager():
    tm = MagicMock()
    tm.commit = Mock()
    tm.rollback = Mock()
    return tm


@pytest.fixture
def mock_job_repo():
    return Mock(spec=JobRepository)


@pytest.fixture
def mock_queue():
    return Mock(spec=BaseQueue)


@pytest.fixture
def job_service(mock_job_repo, mock_transaction_manager, mock_queue):
    return JobService(
        job_repository=mock_job_repo,
        transaction_manager=mock_transaction_manager,
        queue=mock_queue,
    )


def test_submit_job_success(job_service, mock_job_repo, mock_queue):
    request = JobSubmissionRequest(
        name="daily_analysis",
        job_type=JobType.WORKLOAD_ANALYSIS,
        payload={"param": 1}
    )
    
    # Mock save to return the same job it was passed
    def mock_save(job: Job) -> Job:
        return job
        
    mock_job_repo.save.side_effect = mock_save
    
    summary = job_service.submit_job(request)
    
    assert summary.name == "daily_analysis"
    assert summary.job_type == JobType.WORKLOAD_ANALYSIS
    assert summary.status == JobStatus.QUEUED
    
    assert mock_queue.enqueue.called
    entry = mock_queue.enqueue.call_args[0][0]
    assert isinstance(entry, QueueEntry)
    assert entry.execution.job.source == "scheduler"


def test_submit_job_queue_failure(job_service, mock_job_repo, mock_queue):
    request = JobSubmissionRequest(
        name="daily_analysis",
        job_type=JobType.WORKLOAD_ANALYSIS,
        payload={"param": 1}
    )
    
    def mock_save(job: Job) -> Job:
        return job
        
    mock_job_repo.save.side_effect = mock_save
    mock_queue.enqueue.side_effect = Exception("Queue full")
    
    with pytest.raises(Exception, match="Queue full"):
        job_service.submit_job(request)
    
    # We expect repo.save to be called with FAILED status
    saved_jobs = [call_args[0][0] for call_args in mock_job_repo.save.call_args_list]
    assert saved_jobs[-1].status == JobStatus.FAILED
    assert saved_jobs[-1].error_message == "Queue full"


def test_get_job_success(job_service, mock_job_repo):
    job_id = uuid4()
    mock_job = Job(name="test", job_type=JobType.MAINTENANCE, payload={}, job_id=job_id)
    mock_job_repo.get.return_value = mock_job
    
    detail = job_service.get_job(job_id)
    assert detail.job_id == job_id
    assert detail.payload == {}


def test_get_job_not_found(job_service, mock_job_repo):
    mock_job_repo.get.return_value = None
    
    with pytest.raises(JobNotFoundError):
        job_service.get_job(uuid4())


def test_list_jobs(job_service, mock_job_repo):
    mock_job1 = Job(name="test1", job_type=JobType.MAINTENANCE, payload={})
    mock_job2 = Job(name="test2", job_type=JobType.MAINTENANCE, payload={})
    
    mock_job_repo.list_jobs.return_value = ([mock_job1, mock_job2], 2)
    
    response = job_service.list_jobs(limit=10)
    assert response.total_count == 2
    assert len(response.jobs) == 2
    assert response.jobs[0].name == "test1"
