from abc import ABC
from abc import abstractmethod
from uuid import UUID

from backend.platform.projects.dto.create_project_request import (
    CreateProjectRequest,
)
from backend.platform.projects.dto.project_response import ProjectResponse


class ProjectService(ABC):
    """
    Application service responsible for project workflows.
    """

    @abstractmethod
    def create(
        self,
        organization_id: UUID,
        request: CreateProjectRequest,
    ) -> ProjectResponse:
        """
        Create a new project within an organization.
        """
        raise NotImplementedError

    @abstractmethod
    def get(
        self,
        project_id: UUID,
    ) -> ProjectResponse | None:
        """
        Retrieve a project by its identifier.
        """
        raise NotImplementedError

    @abstractmethod
    def list_by_organization(
        self,
        organization_id: UUID,
    ) -> list[ProjectResponse]:
        """
        Retrieve all projects belonging to an organization.
        """
        raise NotImplementedError