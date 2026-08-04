from abc import ABC
from abc import abstractmethod
from uuid import UUID

from backend.platform.apis.domain.api import Api


class ApiRepository(
    ABC,
):
    @abstractmethod
    def create(
        self,
        api: Api,
    ) -> Api:
        raise NotImplementedError

    @abstractmethod
    def update(
        self,
        api: Api,
    ) -> Api:
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        api_id: UUID,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(
        self,
        api_id: UUID,
    ) -> Api | None:
        raise NotImplementedError

    @abstractmethod
    def list_by_environment(
        self,
        environment_id: UUID,
    ) -> list[Api]:
        raise NotImplementedError

    @abstractmethod
    def exists_by_slug(
        self,
        environment_id: UUID,
        slug: str,
    ) -> bool:
        raise NotImplementedError