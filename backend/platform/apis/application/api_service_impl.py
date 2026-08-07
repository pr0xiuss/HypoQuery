from datetime import UTC
from datetime import datetime
from uuid import UUID
from uuid import uuid4

from backend.platform.shared.slug import generate_slug

from backend.platform.apis.service.api_service import ApiService
from backend.platform.apis.domain.api import Api
from backend.platform.apis.dto.api_response import ApiResponse
from backend.platform.apis.dto.create_api_request import CreateApiRequest
from backend.platform.apis.dto.update_api_request import UpdateApiRequest
from backend.platform.apis.repositories.api_repo import ApiRepository


class ApiServiceImpl(ApiService):
    """
    Default implementation of the API service.
    """

    def __init__(
        self,
        repository: ApiRepository,
    ):
        self._repository = repository

    def create(
        self,
        environment_id: UUID,
        request: CreateApiRequest,
    ) -> ApiResponse:
        slug = generate_slug(
            request.name,
        )

        if self._repository.exists_by_slug(
            environment_id,
            slug,
        ):
            raise ValueError(
                "API with this name already exists.",
            )

        now = datetime.now(UTC)

        api = Api(
            id=uuid4(),
            environment_id=environment_id,
            name=request.name,
            slug=slug,
            method=request.method,
            path=request.path,
            description=request.description,
            framework=request.framework,
            base_url=request.base_url,
            version=request.version,
            is_active=request.is_active,
            created_at=now,
            updated_at=now,
        )

        saved_api = self._repository.create(
            api,
        )

        return self._to_response(
            saved_api,
        )

    def get(
        self,
        api_id: UUID,
    ) -> ApiResponse | None:
        api = self._repository.get_by_id(
            api_id,
        )

        if api is None:
            return None

        return self._to_response(
            api,
        )

    def list(
        self,
        environment_id: UUID,
    ) -> list[ApiResponse]:
        apis = self._repository.list_by_environment(
            environment_id,
        )

        return [
            self._to_response(
                api,
            )
            for api in apis
        ]

    def update(
        self,
        api_id: UUID,
        request: UpdateApiRequest,
    ) -> ApiResponse:
        api = self._repository.get_by_id(
            api_id,
        )

        if api is None:
            raise ValueError(
                "API not found.",
            )

        slug = generate_slug(
            request.name,
        )

        if (
            slug != api.slug
            and self._repository.exists_by_slug(
                api.environment_id,
                slug,
            )
        ):
            raise ValueError(
                "API with this name already exists.",
            )

        updated_api = api.model_copy(
            update={
                "name": request.name,
                "slug": slug,
                "method": request.method,
                "path": request.path,
                "description": request.description,
                "framework": request.framework,
                "base_url": request.base_url,
                "version": request.version,
                "is_active": request.is_active,
                "updated_at": datetime.now(
                    UTC,
                ),
            },
        )

        updated_api = self._repository.update(
            updated_api,
        )

        return self._to_response(
            updated_api,
        )

    def delete(
        self,
        api_id: UUID,
    ) -> None:
        self._repository.delete(
            api_id,
        )

    @staticmethod
    def _to_response(
        api: Api,
    ) -> ApiResponse:
        return ApiResponse(
            id=api.id,
            environment_id=api.environment_id,
            name=api.name,
            slug=api.slug,
            description=api.description,
            framework=api.framework,
            base_url=api.base_url,
            version=api.version,
            is_active=api.is_active,
            created_at=api.created_at,
            updated_at=api.updated_at,
        )