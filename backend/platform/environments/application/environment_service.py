from abc import ABC
from abc import abstractmethod
from uuid import UUID
from backend.platform.environments.dto.create_environment_request import CreateEnvironmentRequest
from backend.platform.environments.dto.environment_response import EnvironmentResponse
from backend.platform.environments.dto.update_env_request import UpdateEnvironmentRequest

class EnvironmentService(ABC):
    """
    Application service responsible for environment workflows.
    """

    @abstractmethod
    def create(
        self,
        project_id: UUID,
        request: CreateEnvironmentRequest,
    ) -> EnvironmentResponse:
        """
        Create a new environment within a project.
        """
        raise NotImplementedError

    @abstractmethod
    def get(
        self,
        environment_id: UUID,
    ) -> EnvironmentResponse | None:
        """
        Retrieve an environment by its identifier.
        """
        raise NotImplementedError

    @abstractmethod
    def list_by_project(
        self,
        project_id: UUID,
    ) -> list[EnvironmentResponse]:
        """
        Retrieve all environments belonging to a project.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        project_id: UUID,
        environment_id: UUID,
    ) -> None:
        """
        Delete an environment belonging to a project.
        """
        raise NotImplementedError

    @abstractmethod
    def update(
        self,
        project_id: UUID,
        environment_id: UUID,
        request: UpdateEnvironmentRequest,
    ) -> EnvironmentResponse:
        """
        Update an existing environment.
        """
        raise NotImplementedError