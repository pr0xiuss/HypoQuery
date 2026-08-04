from abc import ABC
from abc import abstractmethod
from uuid import UUID
from backend.platform.environments.domain.environment import Environment


class EnvironmentRepository(ABC):
    """
    Repository contract for environment persistence.
    """

    @abstractmethod
    def save(
        self,
        environment: Environment,
    ) -> Environment:
        """
        Persist an environment.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_id(
        self,
        environment_id: UUID,
    ) -> Environment | None:
        """
        Retrieve an environment by its identifier.
        """
        raise NotImplementedError

    @abstractmethod
    def list_by_project(
        self,
        project_id: UUID,
    ) -> list[Environment]:
        """
        Retrieve all environments belonging to a project.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_project_and_slug(
        self,
        project_id: UUID,
        slug: str,
    ) -> Environment | None:
        """
        Determine whether an environment with the given name already
        exists within a project.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        environment_id: UUID,
    ) -> None:
        """
        Delete an environment.
        """
        raise NotImplementedError

    @abstractmethod
    def update(
        self,
        environment: Environment,
    ) -> Environment:
        """
        Update an existing environment.
        """
        raise NotImplementedError