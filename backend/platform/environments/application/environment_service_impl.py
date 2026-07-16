from datetime import UTC
from datetime import datetime
from uuid import UUID
from uuid import uuid4

from backend.platform.environments.application.environment_service import (
    EnvironmentService,
)
from backend.platform.environments.domain.environment import (
    Environment,
)
from backend.platform.environments.dto.create_environment_request import (
    CreateEnvironmentRequest,
)
from backend.platform.environments.dto.environment_response import (
    EnvironmentResponse,
)
from backend.platform.environments.repositories.environment_repository import (
    EnvironmentRepository,
)


class EnvironmentServiceImpl(EnvironmentService):
    """
    Default implementation of the environment application service.
    """

    def __init__(
        self,
        environment_repository: EnvironmentRepository,
    ) -> None:
        self._environment_repository = environment_repository

    def create(
        self,
        project_id: UUID,
        request: CreateEnvironmentRequest,
    ) -> EnvironmentResponse:
        now = datetime.now(UTC)

        environment = Environment(
            id=uuid4(),
            project_id=project_id,
            name=request.name,
            description=request.description,
            created_at=now,
            updated_at=now,
        )

        persisted_environment = self._environment_repository.save(
            environment,
        )

        return EnvironmentResponse(
            id=persisted_environment.id,
            project_id=persisted_environment.project_id,
            name=persisted_environment.name,
            description=persisted_environment.description,
            created_at=persisted_environment.created_at,
            updated_at=persisted_environment.updated_at,
        )
    

    def get(
        self,
        environment_id: UUID,
    ) -> EnvironmentResponse | None:
        environment = self._environment_repository.get_by_id(
            environment_id,
        )

        if environment is None:
            return None

        return EnvironmentResponse(
            id=environment.id,
            project_id=environment.project_id,
            name=environment.name,
            description=environment.description,
            created_at=environment.created_at,
            updated_at=environment.updated_at,
        )
    

    def list_by_project(
        self,
        project_id: UUID,
    ) -> list[EnvironmentResponse]:
        environments = self._environment_repository.list_by_project(
            project_id,
        )

        return [
            EnvironmentResponse(
                id=environment.id,
                project_id=environment.project_id,
                name=environment.name,
                description=environment.description,
                created_at=environment.created_at,
                updated_at=environment.updated_at,
            )
            for environment in environments
        ]