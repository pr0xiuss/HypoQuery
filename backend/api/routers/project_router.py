from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi import HTTPException
from backend.api.dependencies import get_project_service
from backend.platform.projects.application.project_service import ProjectService
from backend.platform.projects.dto.create_project_request import CreateProjectRequest
from backend.platform.projects.dto.update_project_request import UpdateProjectRequest
from backend.platform.projects.dto.project_response import ProjectResponse


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

@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    status_code=status.HTTP_200_OK,
)
def get_project(
    organization_id: UUID,
    project_id: UUID,
    service: ProjectService = Depends(get_project_service),
) -> ProjectResponse:
    project = service.get(project_id)

    if project is None or project.organization_id != organization_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return project

@router.get(
    "",
    response_model=list[ProjectResponse],
    status_code=status.HTTP_200_OK,
)
def list_projects(
    organization_id: UUID,
    service: ProjectService = Depends(
        get_project_service,
    ),
) -> list[ProjectResponse]:
    """
    List all projects within an organization.
    """

    return service.list_by_organization(
        organization_id=organization_id,
    )

@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_project(
    organization_id: UUID,
    project_id: UUID,
    service: ProjectService = Depends(
        get_project_service,
    ),
) -> None:
    """
    Delete a project.
    """

    service.delete(
        organization_id=organization_id,
        project_id=project_id,
    )

@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
    status_code=status.HTTP_200_OK,
)
def update_project(
    organization_id: UUID,
    project_id: UUID,
    request: UpdateProjectRequest,
    service: ProjectService = Depends(
        get_project_service,
    ),
) -> ProjectResponse:
    """
    Update a project.
    """

    project = service.update(
        organization_id=organization_id,
        project_id=project_id,
        request=request,
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    return project