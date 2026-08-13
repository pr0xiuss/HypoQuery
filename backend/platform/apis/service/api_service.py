from __future__ import annotations
from abc import ABC
from abc import abstractmethod
from uuid import UUID
from backend.platform.apis.domain.api_endpoint import ApiEndpoint
from backend.platform.apis.domain.api import Api
from backend.platform.apis.dto.create_api_request import CreateApiRequest
from backend.platform.apis.dto.update_api_request import UpdateApiRequest


class ApiService(
    ABC,
):
    @abstractmethod
    def create(
        self,
        environment_id: UUID,
        request: CreateApiRequest,
    ) -> Api:
        raise NotImplementedError

    @abstractmethod
    def update(
        self,
        api_id: UUID,
        request: UpdateApiRequest,
    ) -> Api:
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        api_id: UUID,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(
        self,
        api_id: UUID,
    ) -> Api:
        raise NotImplementedError

    @abstractmethod
    def list(
        self,
        environment_id: UUID,
    ) -> list[Api]:
        raise NotImplementedError

    @abstractmethod
    def list_endpoints(
        self,
        api_id: UUID,
    ) -> list[ApiEndpoint]:
        raise NotImplementedError