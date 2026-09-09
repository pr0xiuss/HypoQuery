import logging

from backend.platform.scheduler.application.job_service import JobService
from backend.platform.scheduler.repositories.job_repository import JobRepository
from backend.execution.runtime.system_clock import SystemClock
from backend.platform.shared.transactions.transaction_manager import TransactionManager


logger = logging.getLogger(__name__)


class RetryOrchestrator:
    """
    Polls for jobs that are in PENDING_RETRY status and have reached their next_attempt_at time,
    and submits them for a new retry attempt via the JobService.
    
    This is conceptually similar to the Scheduler daemon but handles backoff retries 
    without interpreting pipeline failures (which is done by the subscriber).
    """

    def __init__(
        self,
        job_repository: JobRepository,
        job_service: JobService,
        clock: SystemClock,
        transaction_manager: TransactionManager,
    ):
        self._job_repository = job_repository
        self._job_service = job_service
        self._clock = clock
        self._transaction_manager = transaction_manager

    def process_due_retries(self, batch_size: int = 50) -> int:
        """
        Queries due retries and processes them one by one.
        Returns the number of retries processed.
        """
        processed_count = 0
        
        for _ in range(batch_size):
            if not self._process_next_due_retry():
                break
            processed_count += 1
            
        return processed_count

    def _process_next_due_retry(self) -> bool:
        """
        Fetches and processes exactly one due retry in an isolated transaction.
        """
        try:
            now = self._clock.now()
            jobs = self._job_repository.get_jobs_due_for_retry(now=now, batch_size=1)
            
            if not jobs:
                self._transaction_manager.rollback()
                return False
                
            job = jobs[0]
            
            # Submitting the job for retry. JobService will update state and commit the transaction.
            self._job_service.retry_job(job.job_id)
            
            logger.info(f"Processed retry for job {job.job_id}. Attempt {job.attempt_count + 1}.")
            return True
            
        except Exception as e:
            logger.error(f"Failed to process retry for job: {e}")
            self._transaction_manager.rollback()
            return False
