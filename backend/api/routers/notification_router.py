from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from dependency_injector.wiring import Provide, inject

from backend.api.dependencies import get_current_user
from backend.platform.auth.domain.user import User
from backend.platform.bootstrap.container import PlatformContainer
from backend.platform.notifications.domain.notification import NotificationType
from backend.platform.notifications.domain.preference import NotificationPreference
from backend.platform.notifications.repositories.notification_repository import NotificationRepository
from backend.platform.notifications.repositories.preference_repository import NotificationPreferenceRepository

router = APIRouter(prefix="/api/v1/notifications", tags=["Notifications"])


class NotificationDTO(BaseModel):
    notification_id: UUID
    notification_type: str
    job_id: Optional[UUID]
    title: str
    message: str
    is_read: bool


class PreferenceUpdateDTO(BaseModel):
    notification_type: str
    is_enabled: bool


@router.get("", response_model=List[NotificationDTO])
@inject
def list_notifications(
    limit: int = 50,
    offset: int = 0,
    user: User = Depends(get_current_user),
    notification_repo: NotificationRepository = Depends(Provide[PlatformContainer.notification_repository]),
):

    notifications = notification_repo.list_for_user(user.id, limit=limit, offset=offset)
    return [
        NotificationDTO(
            notification_id=n.notification_id,
            notification_type=n.notification_type.value,
            job_id=n.job_id,
            title=n.title,
            message=n.message,
            is_read=n.is_read
        )
        for n in notifications
    ]


@router.patch("/{notification_id}/read", response_model=NotificationDTO)
@inject
def mark_read(
    notification_id: UUID,
    user: User = Depends(get_current_user),
    notification_repo: NotificationRepository = Depends(Provide[PlatformContainer.notification_repository]),
):

    notification = notification_repo.get(notification_id)
    if not notification or notification.user_id != user.id:
        raise HTTPException(status_code=404, detail="Notification not found")

    updated = notification.mark_read()
    saved = notification_repo.save(updated)
    
    return NotificationDTO(
        notification_id=saved.notification_id,
        notification_type=saved.notification_type.value,
        job_id=saved.job_id,
        title=saved.title,
        message=saved.message,
        is_read=saved.is_read
    )


@router.get("/preferences", response_model=List[PreferenceUpdateDTO])
@inject
def get_preferences(
    user: User = Depends(get_current_user),
    preference_repo: NotificationPreferenceRepository = Depends(Provide[PlatformContainer.notification_preference_repository]),
):

    prefs = preference_repo.list_for_user(user.id)
    return [
        PreferenceUpdateDTO(
            notification_type=p.notification_type.value,
            is_enabled=p.is_enabled
        )
        for p in prefs
    ]


@router.put("/preferences", response_model=PreferenceUpdateDTO)
@inject
def update_preference(
    update_req: PreferenceUpdateDTO,
    user: User = Depends(get_current_user),
    preference_repo: NotificationPreferenceRepository = Depends(Provide[PlatformContainer.notification_preference_repository]),
):

    try:
        ntype = NotificationType(update_req.notification_type)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid notification type")

    pref = preference_repo.get_by_user_and_type(user.id, ntype)
    if pref:
        pref = pref.with_status(update_req.is_enabled)
    else:
        pref = NotificationPreference(
            user_id=user.id,
            notification_type=ntype,
            is_enabled=update_req.is_enabled
        )

    saved = preference_repo.save(pref)
    return PreferenceUpdateDTO(
        notification_type=saved.notification_type.value,
        is_enabled=saved.is_enabled
    )
