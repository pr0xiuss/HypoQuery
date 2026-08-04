from datetime import UTC
from datetime import datetime
from uuid import UUID
from uuid import uuid4
from backend.platform.shared.slug import generate_slug
from backend.platform.environments.application.environment_service import EnvironmentService
from backend.platform.environments.domain.environment import Environment
from backend.platform.environments.dto.create_environment_request import CreateEnvironmentRequest
from backend.platform.environments.dto.environment_response import EnvironmentResponse
from backend.platform.environments.repositories.environment_repository import EnvironmentRepository
from backend.platform.environments.dto.update_env_request import UpdateEnvironmentRequest

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
        slug = generate_slug(request.name)

        existing = (
            self._environment_repository.get_by_project_and_slug(
                project_id=project_id,
                slug=slug,
            )
        )

        if existing is not None:
            raise ValueError(
                "Environment slug already exists",
            )

        environment = Environment(
            id=uuid4(),
            project_id=project_id,
            name=request.name,
            description=request.description,
            slug=slug,
            environment_type=request.type,
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
            slug=persisted_environment.slug,
            type=persisted_environment.environment_type,
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
            slug=environment.slug,
            type=environment.environment_type,
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
                slug=environment.slug,
                type=environment.environment_type,
                created_at=environment.created_at,
                updated_at=environment.updated_at,
            )
            for environment in environments
        ]

    def delete(
        self,
        project_id: UUID,
        environment_id: UUID,
    ) -> None:
        environment = self._environment_repository.get_by_id(
            environment_id,
        )

        if environment is None:
            raise ValueError(
                "Environment not found",
            )

        if environment.project_id != project_id:
            raise ValueError(
                "Environment does not belong to the specified project",
            )

        self._environment_repository.delete(
            environment_id,
        )

    def update(
        self,
        project_id: UUID,
        environment_id: UUID,
        request: UpdateEnvironmentRequest,
    ) -> EnvironmentResponse:
        environment = self._environment_repository.get_by_id(
            environment_id,
        )

        if environment is None:
            raise ValueError(
                "Environment not found",
            )

        if environment.project_id != project_id:
            raise ValueError(
                "Environment does not belong to the specified project",
            )

        slug = generate_slug(
            request.name,
        )

        existing = (
            self._environment_repository.get_by_project_and_slug(
                project_id=project_id,
                slug=slug,
            )
        )

        if (
            existing is not None
            and existing.id != environment.id
        ):
            raise ValueError(
                "Environment slug already exists",
            )

        updated_environment = environment.model_copy(
            update={
                "name": request.name,
                "description": request.description,
                "slug": slug,
                "environment_type": request.type,
                "updated_at": datetime.now(UTC),
            },
        )

        persisted_environment = (
            self._environment_repository.update(
                updated_environment,
            )
        )

        return EnvironmentResponse(
            id=persisted_environment.id,
            project_id=persisted_environment.project_id,
            name=persisted_environment.name,
            description=persisted_environment.description,
            slug=persisted_environment.slug,
            type=persisted_environment.environment_type,
            created_at=persisted_environment.created_at,
            updated_at=persisted_environment.updated_at,
        )