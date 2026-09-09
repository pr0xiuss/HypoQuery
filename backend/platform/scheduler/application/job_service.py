from uuid import UUID, uuid4

from backend.execution.contracts.context import PipelineContext
from backend.execution.contracts.execution import PipelineExecution
from backend.execution.contracts.job import PipelineJob
from backend.execution.queue.base_queue import BaseQueue
from backend.execution.queue.job_record import QueueEntry

from backend.platform.scheduler.application.dtos import (
    JobDetailDTO,
    JobListResponse,
    JobSubmissionRequest,
    JobSummaryDTO,
)
from backend.platform.scheduler.domain.job import Job, JobStatus
from backend.platform.scheduler.repositories.job_repository import JobRepository
from backend.platform.shared.transactions.transaction_manager import TransactionManager


class JobNotFoundError(Exception):
    pass


class JobService:
    """
    Application service orchestrating background jobs.
    
    Responsible for accepting job requests and persisting them.
    In later batches, this will also push to the execution queue.
    """

    def __init__(
        self,
        job_repository: JobRepository,
        transaction_manager: TransactionManager,
        queue: BaseQueue,
    ):
        self._job_repository = job_repository
        self._transaction_manager = transaction_manager
        self._queue = queue

    def submit_job(self, request: JobSubmissionRequest) -> JobSummaryDTO:
        """
        Submits a new background job request.
        """
        job = Job(
            name=request.name,
            job_type=request.job_type,
            payload=request.payload,
            project_id=request.project_id,
            environment_id=request.environment_id,
            status=JobStatus.PENDING,
        )

        try:
            saved_job = self._job_repository.save(job)
            
            # Map Platform Job to Execution Contracts
            execution_id = uuid4()
            trace_id = uuid4()
            
            pipeline_job = PipelineJob(
                source="scheduler",
                pipeline_version="1.0",
                job_id=saved_job.job_id,
                trace_id=trace_id,
            )
            
            context = PipelineContext(
                execution_id=execution_id,
                trace_id=trace_id,
                pipeline_name=saved_job.job_type.value,
                pipeline_version="1.0",
                database=saved_job.payload.get("database", "postgres"),
                schema=saved_job.payload.get("schema", "public"),
                metadata={
                    "platform_job_id": str(saved_job.job_id),
                    "job_attempt_count": saved_job.attempt_count + 1,
                    "job_max_attempts": saved_job.max_attempts,
                }
            )
            
            execution = PipelineExecution(
                job=pipeline_job,
                context=context
            )
            queue_entry = QueueEntry(execution=execution)
            
            try:
                self._queue.enqueue(queue_entry)
                # Enqueue succeeded, update status
                saved_job = saved_job.with_status(JobStatus.QUEUED, execution_id=execution_id)
                saved_job = self._job_repository.save(saved_job)
                self._transaction_manager.commit()
            except Exception as e:
                # Enqueue failed, update status to FAILED
                saved_job = saved_job.with_status(JobStatus.FAILED, error_message=str(e))
                saved_job = self._job_repository.save(saved_job)
                self._transaction_manager.commit()
                raise

        except Exception:
            self._transaction_manager.rollback()
            raise

        return self._to_summary_dto(saved_job)

    def retry_job(self, job_id: UUID) -> JobSummaryDTO:
        """
        Retries an existing background job that is in PENDING_RETRY status.
        Creates a new execution attempt and enqueues it.
        """
        job = self._job_repository.get(job_id)
        if not job:
            raise JobNotFoundError(f"Job {job_id} not found")
            
        if job.status != JobStatus.PENDING_RETRY:
            raise ValueError(f"Job {job_id} is in status {job.status.value}, expected PENDING_RETRY")
            
        execution_id = uuid4()
        trace_id = uuid4()
        
        pipeline_job = PipelineJob(
            source="scheduler",
            pipeline_version="1.0",
            job_id=job.job_id,
            trace_id=trace_id,
        )
        
        context = PipelineContext(
            execution_id=execution_id,
            trace_id=trace_id,
            pipeline_name=job.job_type.value,
            pipeline_version="1.0",
            database=job.payload.get("database", "postgres"),
            schema=job.payload.get("schema", "public"),
            metadata={
                "platform_job_id": str(job.job_id),
                "job_attempt_count": job.attempt_count + 1,
                "job_max_attempts": job.max_attempts,
            }
        )
        
        execution = PipelineExecution(
            job=pipeline_job,
            context=context
        )
        queue_entry = QueueEntry(execution=execution)
        
        try:
            self._queue.enqueue(queue_entry)
            job = job.with_status(JobStatus.QUEUED, execution_id=execution_id)
            saved_job = self._job_repository.save(job)
            self._transaction_manager.commit()
            return self._to_summary_dto(saved_job)
        except Exception as e:
            self._transaction_manager.rollback()
            raise

    def get_job(self, job_id: UUID) -> JobDetailDTO:
        """
        Retrieves detailed information about a job.
        """
        with self._transaction_manager.atomic():
            job = self._job_repository.get(job_id)
            if not job:
                raise JobNotFoundError(f"Job {job_id} not found")
            return self._to_detail_dto(job)

    def list_jobs(self, limit: int = 100, offset: int = 0) -> JobListResponse:
        """
        Lists jobs with pagination.
        """
        with self._transaction_manager.atomic():
            jobs, total_count = self._job_repository.list_jobs(limit=limit, offset=offset)

        summaries = [self._to_summary_dto(j) for j in jobs]
        return JobListResponse(
            jobs=summaries,
            total_count=total_count,
            limit=limit,
            offset=offset,
        )

    def cancel_job(self, job_id: UUID) -> None:
        """
        Cancels a background job.
        
        Currently unsupported due to lack of safe interruption in PipelineExecutor.
        """
        raise NotImplementedError("Job cancellation is not supported in the existing synchronous execution framework.")

    def _to_summary_dto(self, job: Job) -> JobSummaryDTO:
        return JobSummaryDTO(
            job_id=job.job_id,
            name=job.name,
            job_type=job.job_type,
            status=job.status,
            created_at=job.created_at,
            updated_at=job.updated_at,
            execution_id=job.execution_id,
        )

    def _to_detail_dto(self, job: Job) -> JobDetailDTO:
        return JobDetailDTO(
            job_id=job.job_id,
            name=job.name,
            job_type=job.job_type,
            status=job.status,
            created_at=job.created_at,
            updated_at=job.updated_at,
            execution_id=job.execution_id,
            payload=job.payload,
            project_id=job.project_id,
            environment_id=job.environment_id,
            error_message=job.error_message,
        )
