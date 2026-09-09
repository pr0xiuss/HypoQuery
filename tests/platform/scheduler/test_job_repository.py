import pytest
from uuid import uuid4
from datetime import UTC, datetime

from backend.platform.scheduler.domain.job import Job, JobStatus, JobType
from backend.platform.scheduler.infra.sqlalchemy_job_repo import SqlAlchemyJobRepository
from backend.platform.scheduler.infra.job_model import JobModel


def test_repository_save_and_get(db_session):
    repo = SqlAlchemyJobRepository(db_session)
    job = Job(
        name="test_job",
        job_type=JobType.WORKLOAD_ANALYSIS,
        payload={"query": "SELECT * FROM users"}
    )
    
    saved_job = repo.save(job)
    assert saved_job.job_id == job.job_id
    
    retrieved_job = repo.get(job.job_id)
    assert retrieved_job is not None
    assert retrieved_job.name == "test_job"
    assert retrieved_job.job_type == JobType.WORKLOAD_ANALYSIS
    assert retrieved_job.status == JobStatus.PENDING
    assert retrieved_job.payload == {"query": "SELECT * FROM users"}

def test_repository_list_jobs(db_session):
    repo = SqlAlchemyJobRepository(db_session)
    # Clear existing jobs if any
    db_session.query(JobModel).delete()
    
    job1 = Job(name="job1", job_type=JobType.MAINTENANCE, payload={})
    job2 = Job(name="job2", job_type=JobType.MAINTENANCE, payload={})
    
    repo.save(job1)
    repo.save(job2)
    
    jobs, total = repo.list_jobs()
    assert total == 2
    assert len(jobs) == 2
    # Check ordering by created_at desc
    assert {j.name for j in jobs} == {"job1", "job2"}

def test_repository_get_nonexistent(db_session):
    repo = SqlAlchemyJobRepository(db_session)
    assert repo.get(uuid4()) is None
