from abc import ABC
from abc import abstractmethod
from uuid import UUID

from backend.platform.environments.dto.create_environment_request import (
    CreateEnvironmentRequest,
)
from backend.platform.environments.dto.environment_response import (
    EnvironmentResponse,
)


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