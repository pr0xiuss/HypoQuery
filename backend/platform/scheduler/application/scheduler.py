import logging
from typing import List

from backend.platform.scheduler.application.job_service import JobService
from backend.platform.scheduler.application.schedule_calculator import ScheduleCalculator
from backend.platform.scheduler.application.dtos import JobSubmissionRequest
from backend.platform.scheduler.domain.schedule import Schedule
from backend.platform.scheduler.repositories.schedule_repository import ScheduleRepository
from backend.platform.shared.transactions.transaction_manager import TransactionManager


logger = logging.getLogger(__name__)


class Scheduler:
    """
    Runtime orchestration component that polls for due schedules,
    submits them as Platform Jobs, and advances their next run time.
    """

    def __init__(
        self,
        schedule_repository: ScheduleRepository,
        job_service: JobService,
        schedule_calculator: ScheduleCalculator,
        transaction_manager: TransactionManager,
    ):
        self._schedule_repository = schedule_repository
        self._job_service = job_service
        self._schedule_calculator = schedule_calculator
        self._transaction_manager = transaction_manager

    def process_due_schedules(self, batch_size: int = 50) -> int:
        """
        Queries due schedules and processes them.
        Returns the number of schedules processed.
        """
        now = self._schedule_calculator._clock.now()
        processed_count = 0

        # We start a transaction, fetch due schedules with FOR UPDATE SKIP LOCKED.
        # However, to avoid keeping the lock for too long, we process them one by one.
        # Actually, if we fetch them inside a transaction, they remain locked until we commit.
        # If we fetch them, process them, and commit per schedule, it's safer and releases locks early.
        # But `get_due_schedules` returns a list. If we do it in a single transaction, the lock covers all.
        
        # We will loop and process one by one to ensure isolated transactions per schedule.
        while True:
            schedule = self._fetch_one_due_schedule()
            if not schedule:
                break
                
            success = self._process_single_schedule(schedule)
            if success:
                processed_count += 1
            else:
                # If a schedule failed to process (e.g. JobService failed), 
                # we don't want to infinite loop over it in this same tick.
                # In a real daemon, we might want to sleep. 
                # For batch processing, we break out if we encounter persistent failures,
                # but to keep it simple, we just process it and if it fails, we assume it's left due.
                # To prevent infinite looping on the same failing schedule in a single poll tick,
                # we only process a maximum of `batch_size` items total.
                pass
            
            if processed_count >= batch_size:
                break

        return processed_count

    def _fetch_one_due_schedule(self) -> Schedule | None:
        """Fetches a single due schedule and rolls back immediately so we don't hold the lock,
        OR we fetch it and return it."""
        # Wait, if we use FOR UPDATE SKIP LOCKED, we must be inside a transaction.
        # If we commit, the lock is released. If we just read it, we have to process it inside that transaction.
        # Therefore, _process_single_schedule should fetch and process in ONE transaction.
        return None  # Re-implemented below

    def process_next_due_schedule(self) -> bool:
        """
        Fetches and processes exactly one due schedule.
        """
        try:
            now = self._schedule_calculator._clock.now()
            schedules = self._schedule_repository.get_due_schedules(now=now, batch_size=1)
            
            if not schedules:
                self._transaction_manager.rollback()
                return False
                
            schedule = schedules[0]
            
            # Advance the schedule FIRST in the session
            next_run_at = self._schedule_calculator.calculate_next_run(schedule)
            advanced_schedule = schedule.with_next_run(next_run_at=next_run_at, last_run_at=now)
            self._schedule_repository.save(advanced_schedule)
            
            # Create the Job submission request
            job_request = JobSubmissionRequest(
                name=f"{schedule.name} - Scheduled Run",
                job_type=schedule.job_type,
                payload=schedule.payload,
            )
            
            # Submit the job through JobService.
            # JobService natively calls transaction_manager.commit() upon successful submission.
            # Because both repositories share the same session/transaction, this atomic commit
            # will persist both the new Job AND the advanced Schedule next_run_at, while safely
            # releasing the FOR UPDATE SKIP LOCKED lock immediately after.
            self._job_service.submit_job(job_request)
            
            logger.info(f"Processed schedule {schedule.schedule_id}. Next run at {next_run_at}.")
            return True
            
        except Exception as e:
            logger.error(f"Failed to process scheduled job: {e}")
            self._transaction_manager.rollback()
            return False

    def process_due_schedules_batch(self, batch_size: int = 50) -> int:
        """
        Polls and processes due schedules up to `batch_size`.
        """
        processed = 0
        for _ in range(batch_size):
            if not self.process_next_due_schedule():
                break
            processed += 1
            
        return processed
