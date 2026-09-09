from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import select

from backend.platform.notifications.domain.notification import Notification, NotificationType
from backend.platform.notifications.infra.notification_model import NotificationModel
from backend.platform.notifications.repositories.notification_repository import NotificationRepository


class SQLAlchemyNotificationRepository(NotificationRepository):
    def __init__(self, session: Session):
        self._session = session

    def save(self, notification: Notification) -> Notification:
        model = self._session.query(NotificationModel).filter_by(notification_id=notification.notification_id).first()
        if not model:
            model = NotificationModel(
                notification_id=notification.notification_id,
                user_id=notification.user_id,
                notification_type=notification.notification_type.value,
                job_id=notification.job_id,
                execution_id=notification.execution_id,
                title=notification.title,
                message=notification.message,
                metadata_=notification.metadata,
                is_read=notification.is_read,
                created_at=notification.created_at,
            )
            self._session.add(model)
        else:
            model.is_read = notification.is_read
            
        self._session.flush()
        return self._to_domain(model)

    def get(self, notification_id: UUID) -> Optional[Notification]:
        model = self._session.query(NotificationModel).filter_by(notification_id=notification_id).first()
        return self._to_domain(model) if model else None

    def get_by_idempotency_key(self, job_id: UUID, notification_type: NotificationType, execution_id: UUID) -> Optional[Notification]:
        stmt = select(NotificationModel).where(
            NotificationModel.job_id == job_id,
            NotificationModel.notification_type == notification_type.value,
            NotificationModel.execution_id == execution_id
        )
        model = self._session.execute(stmt).scalar_one_or_none()
        return self._to_domain(model) if model else None

    def list_for_user(self, user_id: UUID, limit: int = 50, offset: int = 0) -> List[Notification]:
        stmt = select(NotificationModel).where(NotificationModel.user_id == user_id).order_by(NotificationModel.created_at.desc()).limit(limit).offset(offset)
        models = self._session.execute(stmt).scalars().all()
        return [self._to_domain(m) for m in models]

    def count_unread_for_user(self, user_id: UUID) -> int:
        stmt = select(NotificationModel).where(
            NotificationModel.user_id == user_id,
            NotificationModel.is_read == False
        )
        return len(self._session.execute(stmt).scalars().all())

    def _to_domain(self, model: NotificationModel) -> Notification:
        return Notification(
            notification_id=model.notification_id,
            user_id=model.user_id,
            notification_type=NotificationType(model.notification_type),
            job_id=model.job_id,
            execution_id=model.execution_id,
            title=model.title,
            message=model.message,
            metadata=model.metadata_,
            is_read=model.is_read,
            created_at=model.created_at
        )
