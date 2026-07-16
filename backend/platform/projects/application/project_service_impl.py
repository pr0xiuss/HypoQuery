from datetime import UTC
from datetime import datetime
from uuid import UUID
from uuid import uuid4

from backend.platform.projects.application.project_service import (
    ProjectService,
)
from backend.platform.projects.domain.project import Project
from backend.platform.projects.dto.create_project_request import (
    CreateProjectRequest,
)
from backend.platform.projects.dto.project_response import (
    ProjectResponse,
)
from backend.platform.projects.repositories.project_repository import (
    ProjectRepository,
)


class ProjectServiceImpl(ProjectService):
    """
    Default implementation of the project application service.
    """

    def __init__(
        self,
        project_repository: ProjectRepository,
    ) -> None:
        self._project_repository = project_repository

    def create(
        self,
        organization_id: UUID,
        request: CreateProjectRequest,
    ) -> ProjectResponse:
        now = datetime.now(UTC)

        project = Project(
            id=uuid4(),
            organization_id=organization_id,
            name=request.name,
            description=request.description,
            created_at=now,
            updated_at=now,
        )

        persisted_project = self._project_repository.save(
            project,
        )

        return ProjectResponse(
            id=persisted_project.id,
            organization_id=persisted_project.organization_id,
            name=persisted_project.name,
            description=persisted_project.description,
            created_at=persisted_project.created_at,
            updated_at=persisted_project.updated_at,
        )

    def get(
        self,
        project_id: UUID,
    ) -> ProjectResponse | None:
        project = self._project_repository.get_by_id(
            project_id,
        )

        if project is None:
            return None

        return ProjectResponse(
            id=project.id,
            organization_id=project.organization_id,
            name=project.name,
            description=project.description,
            created_at=project.created_at,
            updated_at=project.updated_at,
        )

    def list_by_organization(
        self,
        organization_id: UUID,
    ) -> list[ProjectResponse]:
        projects = self._project_repository.list_by_organization(
            organization_id,
        )

        return [
            ProjectResponse(
                id=project.id,
                organization_id=project.organization_id,
                name=project.name,
                description=project.description,
                created_at=project.created_at,
                updated_at=project.updated_at,
)
            for project in projects
        ]