from typing import List, Optional, Tuple
from uuid import UUID
from datetime import datetime

from sqlalchemy.orm import Session

from backend.platform.scheduler.domain.job import JobType
from backend.platform.scheduler.domain.schedule import Schedule
from backend.platform.scheduler.infra.schedule_model import ScheduleModel
from backend.platform.scheduler.repositories.schedule_repository import ScheduleRepository


class SqlAlchemyScheduleRepository(ScheduleRepository):
    """
    SQLAlchemy implementation of the ScheduleRepository.
    """

    def __init__(self, session: Session):
        self._session = session

    def _to_domain(self, model: ScheduleModel) -> Schedule:
        return Schedule(
            schedule_id=model.schedule_id,
            name=model.name,
            job_type=JobType(model.job_type),
            payload=model.payload,
            interval_seconds=model.interval_seconds,
            is_enabled=model.is_enabled,
            next_run_at=model.next_run_at,
            last_run_at=model.last_run_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, schedule: Schedule, existing: Optional[ScheduleModel] = None) -> ScheduleModel:
        model = existing or ScheduleModel(schedule_id=schedule.schedule_id)
        model.name = schedule.name
        model.job_type = schedule.job_type.value
        model.payload = schedule.payload
        model.interval_seconds = schedule.interval_seconds
        model.is_enabled = schedule.is_enabled
        model.next_run_at = schedule.next_run_at
        model.last_run_at = schedule.last_run_at
        model.created_at = schedule.created_at
        model.updated_at = schedule.updated_at
        return model

    def save(self, schedule: Schedule) -> Schedule:
        model = self._session.query(ScheduleModel).filter_by(schedule_id=schedule.schedule_id).first()
        model = self._to_model(schedule, model)
        
        self._session.add(model)
        self._session.flush()
        
        return self._to_domain(model)

    def get(self, schedule_id: UUID) -> Optional[Schedule]:
        model = self._session.query(ScheduleModel).filter_by(schedule_id=schedule_id).first()
        if not model:
            return None
        return self._to_domain(model)

    def delete(self, schedule_id: UUID) -> None:
        model = self._session.query(ScheduleModel).filter_by(schedule_id=schedule_id).first()
        if model:
            self._session.delete(model)
            self._session.flush()

    def list_schedules(self, limit: int = 100, offset: int = 0) -> Tuple[List[Schedule], int]:
        query = self._session.query(ScheduleModel)
        total_count = query.count()
        
        models = query.order_by(ScheduleModel.created_at.desc()).offset(offset).limit(limit).all()
        return [self._to_domain(m) for m in models], total_count

    def get_due_schedules(self, now: datetime, batch_size: int = 50) -> List[Schedule]:
        # Using with_for_update(skip_locked=True) ensures that if multiple
        # scheduler instances poll at the same time, they won't grab the same schedules.
        models = (
            self._session.query(ScheduleModel)
            .filter(
                ScheduleModel.is_enabled == True,
                ScheduleModel.next_run_at <= now,
            )
            .order_by(ScheduleModel.next_run_at.asc())
            .with_for_update(skip_locked=True)
            .limit(batch_size)
            .all()
        )
        return [self._to_domain(m) for m in models]
