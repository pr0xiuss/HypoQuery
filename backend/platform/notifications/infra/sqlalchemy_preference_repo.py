from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import select

from backend.platform.notifications.domain.notification import NotificationType
from backend.platform.notifications.domain.preference import NotificationPreference
from backend.platform.notifications.infra.preference_model import NotificationPreferenceModel
from backend.platform.notifications.repositories.preference_repository import NotificationPreferenceRepository


class SQLAlchemyPreferenceRepository(NotificationPreferenceRepository):
    def __init__(self, session: Session):
        self._session = session

    def save(self, preference: NotificationPreference) -> NotificationPreference:
        model = self._session.query(NotificationPreferenceModel).filter_by(preference_id=preference.preference_id).first()
        if not model:
            model = NotificationPreferenceModel(
                preference_id=preference.preference_id,
                user_id=preference.user_id,
                notification_type=preference.notification_type.value,
                is_enabled=preference.is_enabled,
                created_at=preference.created_at,
                updated_at=preference.updated_at,
            )
            self._session.add(model)
        else:
            model.is_enabled = preference.is_enabled
            model.updated_at = preference.updated_at
            
        self._session.flush()
        return self._to_domain(model)

    def get_by_user_and_type(self, user_id: UUID, notification_type: NotificationType) -> Optional[NotificationPreference]:
        stmt = select(NotificationPreferenceModel).where(
            NotificationPreferenceModel.user_id == user_id,
            NotificationPreferenceModel.notification_type == notification_type.value
        )
        model = self._session.execute(stmt).scalar_one_or_none()
        return self._to_domain(model) if model else None

    def list_for_user(self, user_id: UUID) -> List[NotificationPreference]:
        stmt = select(NotificationPreferenceModel).where(NotificationPreferenceModel.user_id == user_id)
        models = self._session.execute(stmt).scalars().all()
        return [self._to_domain(m) for m in models]

    def _to_domain(self, model: NotificationPreferenceModel) -> NotificationPreference:
        return NotificationPreference(
            preference_id=model.preference_id,
            user_id=model.user_id,
            notification_type=NotificationType(model.notification_type),
            is_enabled=model.is_enabled,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
