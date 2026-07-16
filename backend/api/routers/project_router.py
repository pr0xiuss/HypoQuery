from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from backend.api.dependencies import get_project_service
from backend.platform.projects.application.project_service import (
    ProjectService,
)
from backend.platform.projects.dto.create_project_request import (
    CreateProjectRequest,
)
from backend.platform.projects.dto.project_response import (
    ProjectResponse,
)

router = APIRouter(
    prefix="/organizations/{organization_id}/projects",
)


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_project(
    organization_id: UUID,
    request: CreateProjectRequest,
    service: ProjectService = Depends(
        get_project_service,
    ),
) -> ProjectResponse:
    """
    Create a project within an organization.
    """

    return service.create(
        organization_id=organization_id,
        request=request,
    )