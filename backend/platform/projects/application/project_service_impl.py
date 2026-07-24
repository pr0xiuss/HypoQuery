from datetime import UTC
from datetime import datetime
from uuid import UUID
from uuid import uuid4

from backend.platform.projects.application.project_service import ProjectService
from backend.platform.projects.domain.project import Project
from backend.platform.projects.dto.create_project_request import CreateProjectRequest
from backend.platform.projects.dto.update_project_request import UpdateProjectRequest
from backend.platform.projects.dto.project_response import ProjectResponse
from backend.platform.projects.repositories.project_repository import ProjectRepository
from backend.platform.shared.slug import generate_slug


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
        slug = generate_slug(request.name)
        existing = self._project_repository.get_by_organization_and_slug(
            organization_id=organization_id,
            slug=slug,
        )

        if existing is not None:
            raise ValueError("Project slug already exists in this organization.")
        
        project = Project(
            id=uuid4(),
            organization_id=organization_id,
            name=request.name,
            description=request.description,
            slug = slug,
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
            slug=persisted_project.slug,
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
            slug=project.slug,
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
                slug=project.slug,
                created_at=project.created_at,
                updated_at=project.updated_at,
)
            for project in projects
        ]


    def delete(
        self,
        organization_id: UUID,
        project_id: UUID,
    ) -> None:
        project = self._project_repository.get_by_id(
            project_id,
        )

        if project is None:
            raise ValueError("Project not found")

        if project.organization_id != organization_id:
            raise ValueError("Project not found")

        self._project_repository.delete(
            project_id,
        )

    def update(
        self,
        organization_id: UUID,
        project_id: UUID,
        request: UpdateProjectRequest,
    ) -> ProjectResponse | None:
        project = self._project_repository.get_by_id(
            project_id,
        )

        if project is None:
            return None

        if project.organization_id != organization_id:
            return None

        slug = generate_slug(request.name)

        existing = self._project_repository.get_by_organization_and_slug(
            organization_id=organization_id,
            slug=slug,
        )

        if existing is not None and existing.id != project.id:
            raise ValueError("Project slug already exists")

        updated_project = project.model_copy(
            update={
                "name": request.name,
                "description": request.description,
                "slug": slug,
                "updated_at": datetime.now(UTC),
            },
        )

        updated_project = self._project_repository.update(
            updated_project,
        )

        return ProjectResponse(
            id=updated_project.id,
            organization_id=updated_project.organization_id,
            name=updated_project.name,
            description=updated_project.description,
            slug=updated_project.slug,
            created_at=updated_project.created_at,
            updated_at=updated_project.updated_at,
        )