from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Query, status

from backend.platform.bootstrap.container import PlatformContainer
from backend.platform.scheduler.application.dtos import (
    ScheduleCreateRequest,
    ScheduleDTO,
    ScheduleListResponse,
    ScheduleUpdateRequest,
)
from backend.platform.scheduler.application.schedule_service import (
    ScheduleNotFoundError,
    ScheduleService,
)


router = APIRouter(prefix="/api/v1/schedules", tags=["Schedules"])


@router.post(
    "",
    response_model=ScheduleDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new schedule",
)
@inject
def create_schedule(
    request: ScheduleCreateRequest,
    schedule_service: ScheduleService = Depends(Provide[PlatformContainer.schedule_service]),
) -> ScheduleDTO:
    """Creates a new recurring schedule."""
    return schedule_service.create_schedule(request)


@router.get(
    "",
    response_model=ScheduleListResponse,
    summary="List schedules",
)
@inject
def list_schedules(
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
    offset: Annotated[int, Query(ge=0)] = 0,
    schedule_service: ScheduleService = Depends(Provide[PlatformContainer.schedule_service]),
) -> ScheduleListResponse:
    """Lists schedules with pagination."""
    return schedule_service.list_schedules(limit=limit, offset=offset)


@router.get(
    "/{schedule_id}",
    response_model=ScheduleDTO,
    summary="Get a schedule",
)
@inject
def get_schedule(
    schedule_id: UUID,
    schedule_service: ScheduleService = Depends(Provide[PlatformContainer.schedule_service]),
) -> ScheduleDTO:
    """Retrieves a single schedule by ID."""
    try:
        return schedule_service.get_schedule(schedule_id)
    except ScheduleNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")


@router.patch(
    "/{schedule_id}",
    response_model=ScheduleDTO,
    summary="Update a schedule",
)
@inject
def update_schedule(
    schedule_id: UUID,
    request: ScheduleUpdateRequest,
    schedule_service: ScheduleService = Depends(Provide[PlatformContainer.schedule_service]),
) -> ScheduleDTO:
    """Updates an existing schedule."""
    try:
        return schedule_service.update_schedule(schedule_id, request)
    except ScheduleNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")


@router.delete(
    "/{schedule_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a schedule",
)
@inject
def delete_schedule(
    schedule_id: UUID,
    schedule_service: ScheduleService = Depends(Provide[PlatformContainer.schedule_service]),
) -> None:
    """Deletes a schedule."""
    try:
        schedule_service.delete_schedule(schedule_id)
    except ScheduleNotFoundError:
        pass
