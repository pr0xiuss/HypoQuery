import pytest
from unittest.mock import Mock, MagicMock
from uuid import uuid4

from backend.execution.contracts.events.pipeline import (
    PipelineStartedEvent,
    PipelineCompletedEvent,
    PipelineFailedEvent,
)
from backend.platform.scheduler.application.job_lifecycle_subscriber import JobLifecycleSubscriber
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
def mock_retry_policy():
    policy = MagicMock()
    # By default, mock not to retry
    policy.calculate_next_attempt.return_value = None
    return policy

@pytest.fixture
def subscriber(mock_job_repo, mock_transaction_manager, mock_retry_policy):
    return JobLifecycleSubscriber(
        job_repository=mock_job_repo,
        transaction_manager=mock_transaction_manager,
        retry_policy=mock_retry_policy,
    )


def test_handle_pipeline_started(subscriber, mock_job_repo):
    execution_id = uuid4()
    job = Job(name="test", job_type=JobType.WORKLOAD_ANALYSIS, payload={}, execution_id=execution_id)
    
    mock_job_repo.get_by_execution_id.return_value = job
    job = job.with_status(JobStatus.QUEUED)
    
    metadata = Mock(execution_id=execution_id)
    event = PipelineStartedEvent(metadata=metadata)
    
    subscriber.handle(event)
    
    mock_job_repo.save.assert_called_once()
    saved_job = mock_job_repo.save.call_args[0][0]
    assert saved_job.status == JobStatus.RUNNING


def test_handle_pipeline_completed(subscriber, mock_job_repo):
    execution_id = uuid4()
    job = Job(name="test", job_type=JobType.WORKLOAD_ANALYSIS, payload={}, execution_id=execution_id)
    job = job.with_status(JobStatus.QUEUED).with_status(JobStatus.RUNNING)
    
    mock_job_repo.get_by_execution_id.return_value = job
    
    metadata = Mock(execution_id=execution_id)
    event = PipelineCompletedEvent(metadata=metadata, duration_ms=100.0)
    
    subscriber.handle(event)
    
    mock_job_repo.save.assert_called_once()
    saved_job = mock_job_repo.save.call_args[0][0]
    assert saved_job.status == JobStatus.COMPLETED


def test_handle_pipeline_failed(subscriber, mock_job_repo):
    execution_id = uuid4()
    job = Job(name="test", job_type=JobType.WORKLOAD_ANALYSIS, payload={}, execution_id=execution_id)
    job = job.with_status(JobStatus.QUEUED).with_status(JobStatus.RUNNING)
    
    mock_job_repo.get_by_execution_id.return_value = job
    
    metadata = Mock(execution_id=execution_id)
    event = PipelineFailedEvent(metadata=metadata, error="Oops")
    
    subscriber.handle(event)
    
    mock_job_repo.save.assert_called_once()
    saved_job = mock_job_repo.save.call_args[0][0]
    assert saved_job.status == JobStatus.FAILED
    assert saved_job.error_message == "Oops"
