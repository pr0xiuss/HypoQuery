from abc import ABC
from abc import abstractmethod
from uuid import UUID

from backend.platform.projects.domain.project import Project


class ProjectRepository(ABC):
    """
    Repository contract for project persistence.
    """

    @abstractmethod
    def save(
        self,
        project: Project,
    ) -> Project:
        """
        Persist a project.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_id(
        self,
        project_id: UUID,
    ) -> Project | None:
        """
        Retrieve a project by its identifier.
        """
        raise NotImplementedError

    @abstractmethod
    def list_by_organization(
        self,
        organization_id: UUID,
    ) -> list[Project]:
        """
        Retrieve all projects belonging to an organization.
        """
        raise NotImplementedError

    @abstractmethod
    def exists_by_name(
        self,
        organization_id: UUID,
        name: str,
    ) -> bool:
        """
        Determine whether a project with the given name already exists
        within an organization.
        """
        raise NotImplementedError