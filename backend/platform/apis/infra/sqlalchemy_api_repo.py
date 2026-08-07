from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.platform.apis.domain.api import Api
from backend.platform.apis.infra.api_model import ApiModel
from backend.platform.apis.repositories.api_repo import ApiRepository

class SqlAlchemyApiRepository(
    ApiRepository,
):
    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def create(
        self,
        api: Api,
    ) -> Api:
        model = ApiModel(
            id=api.id,
            environment_id=api.environment_id,
            name=api.name,
            method=api.method,
            path=api.path,
            slug=api.slug,
            description=api.description,
            framework=api.framework,
            base_url=api.base_url,
            version=api.version,
            is_active=api.is_active,
            created_at=api.created_at,
            updated_at=api.updated_at,
        )

        self._session.add(model)
        self._session.commit()
        self._session.refresh(model)

        return self._to_domain(model)

    def update(
        self,
        api: Api,
    ) -> Api:
        model = self._session.get(
            ApiModel,
            api.id,
        )

        if model is None:
            raise ValueError("API not found.")

        model.name = api.name
        model.slug = api.slug
        model.method = api.method
        model.path = api.path
        model.description = api.description
        model.framework = api.framework
        model.base_url = api.base_url
        model.version = api.version
        model.is_active = api.is_active
        model.updated_at = api.updated_at

        self._session.commit()
        self._session.refresh(model)

        return self._to_domain(model)

    def delete(
        self,
        api_id: UUID,
    ) -> None:
        model = self._session.get(
            ApiModel,
            api_id,
        )

        if model is None:
            raise ValueError("API not found.")

        self._session.delete(model)
        self._session.commit()

    def get_by_id(
        self,
        api_id: UUID,
    ) -> Api | None:
        model = self._session.get(
            ApiModel,
            api_id,
        )

        if model is None:
            return None

        return self._to_domain(model)

    def list_by_environment(
        self,
        environment_id: UUID,
    ) -> list[Api]:
        statement = (
            select(ApiModel)
            .where(
                ApiModel.environment_id == environment_id,
            )
            .order_by(ApiModel.name)
        )

        models = self._session.scalars(statement).all()

        return [
            self._to_domain(model)
            for model in models
        ]

    def exists_by_slug(
        self,
        environment_id: UUID,
        slug: str,
    ) -> bool:
        statement = (
            select(ApiModel.id)
            .where(
                ApiModel.environment_id == environment_id,
                ApiModel.slug == slug,
            )
        )

        return self._session.scalar(statement) is not None

    @staticmethod
    def _to_domain(
        model: ApiModel,
    ) -> Api:
        return Api(
            id=model.id,
            environment_id=model.environment_id,
            name=model.name,
            slug=model.slug,
            method=model.method,
            path=model.path,
            description=model.description,
            framework=model.framework,
            base_url=model.base_url,
            version=model.version,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )