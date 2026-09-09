from typing import Optional
from uuid import uuid4, UUID

from backend.platform.scheduler.application.dtos import (
    ScheduleCreateRequest,
    ScheduleUpdateRequest,
    ScheduleDTO,
    ScheduleListResponse,
)
from backend.platform.scheduler.application.schedule_calculator import ScheduleCalculator
from backend.platform.scheduler.domain.schedule import Schedule
from backend.platform.scheduler.repositories.schedule_repository import ScheduleRepository
from backend.platform.shared.transactions.transaction_manager import TransactionManager


class ScheduleNotFoundError(Exception):
    """Raised when a schedule cannot be found."""


class ScheduleService:
    """
    Application service for managing schedules.
    """

    def __init__(
        self,
        schedule_repository: ScheduleRepository,
        transaction_manager: TransactionManager,
        schedule_calculator: ScheduleCalculator,
    ):
        self._schedule_repository = schedule_repository
        self._transaction_manager = transaction_manager
        self._schedule_calculator = schedule_calculator

    def _to_dto(self, schedule: Schedule) -> ScheduleDTO:
        return ScheduleDTO(
            schedule_id=schedule.schedule_id,
            name=schedule.name,
            job_type=schedule.job_type,
            payload=schedule.payload,
            interval_seconds=schedule.interval_seconds,
            is_enabled=schedule.is_enabled,
            next_run_at=schedule.next_run_at,
            last_run_at=schedule.last_run_at,
            created_at=schedule.created_at or self._schedule_calculator._clock.now(),
            updated_at=schedule.updated_at or self._schedule_calculator._clock.now(),
        )

    def create_schedule(self, request: ScheduleCreateRequest) -> ScheduleDTO:
        """
        Create a new enabled schedule.
        """
        schedule = Schedule(
            schedule_id=uuid4(),
            name=request.name,
            job_type=request.job_type,
            payload=request.payload,
            interval_seconds=request.interval_seconds,
            is_enabled=True,
            next_run_at=self._schedule_calculator._clock.now(), # Due immediately or should it be deferred? We make it due immediately.
        )
        # Advance it? No, if we want it to run immediately upon creation, we can set next_run_at to now.
        # But maybe we want it to wait `interval_seconds` first? Let's make it start now.
        
        try:
            saved_schedule = self._schedule_repository.save(schedule)
            self._transaction_manager.commit()
            return self._to_dto(saved_schedule)
        except Exception:
            self._transaction_manager.rollback()
            raise

    def get_schedule(self, schedule_id: UUID) -> ScheduleDTO:
        """
        Retrieve a schedule by ID.
        """
        schedule = self._schedule_repository.get(schedule_id)
        if not schedule:
            raise ScheduleNotFoundError(f"Schedule {schedule_id} not found.")
        return self._to_dto(schedule)

    def update_schedule(self, schedule_id: UUID, request: ScheduleUpdateRequest) -> ScheduleDTO:
        """
        Update an existing schedule.
        """
        schedule = self._schedule_repository.get(schedule_id)
        if not schedule:
            raise ScheduleNotFoundError(f"Schedule {schedule_id} not found.")

        updated_schedule = Schedule(
            schedule_id=schedule.schedule_id,
            name=request.name if request.name is not None else schedule.name,
            job_type=schedule.job_type,
            payload=request.payload if request.payload is not None else schedule.payload,
            interval_seconds=request.interval_seconds if request.interval_seconds is not None else schedule.interval_seconds,
            is_enabled=request.is_enabled if request.is_enabled is not None else schedule.is_enabled,
            next_run_at=schedule.next_run_at,
            last_run_at=schedule.last_run_at,
            created_at=schedule.created_at,
            updated_at=schedule.updated_at,
        )

        try:
            saved_schedule = self._schedule_repository.save(updated_schedule)
            self._transaction_manager.commit()
            return self._to_dto(saved_schedule)
        except Exception:
            self._transaction_manager.rollback()
            raise

    def delete_schedule(self, schedule_id: UUID) -> None:
        """
        Delete a schedule.
        """
        try:
            self._schedule_repository.delete(schedule_id)
            self._transaction_manager.commit()
        except Exception:
            self._transaction_manager.rollback()
            raise

    def list_schedules(self, limit: int = 100, offset: int = 0) -> ScheduleListResponse:
        """
        List all schedules.
        """
        schedules, total_count = self._schedule_repository.list_schedules(limit, offset)
        return ScheduleListResponse(
            schedules=[self._to_dto(s) for s in schedules],
            total_count=total_count,
            limit=limit,
            offset=offset,
        )
