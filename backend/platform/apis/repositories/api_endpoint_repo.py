from abc import ABC
from abc import abstractmethod
from uuid import UUID

from backend.platform.apis.domain.api_endpoint import (
    ApiEndpoint,
)


class ApiEndpointRepository(
    ABC,
):

    @abstractmethod
    def list_by_api(
        self,
        api_id: UUID,
    ) -> list[ApiEndpoint]:
        ...

    @abstractmethod
    def create(
        self,
        endpoint: ApiEndpoint,
    ) -> ApiEndpoint:
        ...

    @abstractmethod
    def update(
        self,
        endpoint: ApiEndpoint,
    ) -> ApiEndpoint:
        ...

    @abstractmethod
    def delete(
        self,
        endpoint_id: UUID,
    ) -> None:
        ...