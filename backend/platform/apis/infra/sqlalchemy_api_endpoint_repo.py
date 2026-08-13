from pathlib import Path
from uuid import UUID

from sqlalchemy import select

from backend.platform.apis.domain.api_endpoint import (
    ApiEndpoint,
)
from backend.platform.apis.infra.api_endpoint_model import (
    ApiEndpointModel,
)
from backend.platform.apis.repositories.api_endpoint_repo import (
    ApiEndpointRepository,
)
from backend.platform.shared.database import (
    SessionLocal,
)


class SQLAlchemyApiEndpointRepository(
    ApiEndpointRepository,
):
    """
    SQLAlchemy implementation of the API endpoint repository.
    """

    def list_by_api(
        self,
        api_id: UUID,
    ) -> list[ApiEndpoint]:

        with SessionLocal() as session:

            statement = (
                select(ApiEndpointModel)
                .where(
                    ApiEndpointModel.api_id == api_id,
                )
                .order_by(
                    ApiEndpointModel.path,
                    ApiEndpointModel.method,
                )
            )

            models = session.scalars(
                statement,
            ).all()

            return [
                self._to_domain(model)
                for model in models
            ]

    def create(
        self,
        endpoint: ApiEndpoint,
    ) -> ApiEndpoint:

        with SessionLocal() as session:

            model = ApiEndpointModel(
                id=endpoint.id,
                api_id=endpoint.api_id,
                method=endpoint.method,
                path=endpoint.path,
                handler=endpoint.handler,
                source_file=(
                    str(endpoint.source_file)
                    if endpoint.source_file is not None
                    else None
                ),
                line_number=endpoint.line_number,
                summary=endpoint.summary,
                description=endpoint.description,
                tags=endpoint.tags,
                version=endpoint.version,
                authentication_required=(
                    endpoint.authentication_required
                ),
            )

            session.add(model)
            session.commit()
            session.refresh(model)

            return self._to_domain(model)

    def update(
        self,
        endpoint: ApiEndpoint,
    ) -> ApiEndpoint:

        with SessionLocal() as session:

            model = session.get(
                ApiEndpointModel,
                endpoint.id,
            )

            if model is None:
                raise ValueError(
                    f"API endpoint not found: {endpoint.id}",
                )

            model.api_id = endpoint.api_id
            model.method = endpoint.method
            model.path = endpoint.path
            model.handler = endpoint.handler

            model.source_file = (
                str(endpoint.source_file)
                if endpoint.source_file is not None
                else None
            )

            model.line_number = endpoint.line_number
            model.summary = endpoint.summary
            model.description = endpoint.description
            model.tags = endpoint.tags
            model.version = endpoint.version

            model.authentication_required = (
                endpoint.authentication_required
            )

            session.commit()
            session.refresh(model)

            return self._to_domain(model)

    def delete(
        self,
        endpoint_id: UUID,
    ) -> None:

        with SessionLocal() as session:

            model = session.get(
                ApiEndpointModel,
                endpoint_id,
            )

            if model is None:
                return

            session.delete(model)
            session.commit()

    @staticmethod
    def _to_domain(
        model: ApiEndpointModel,
    ) -> ApiEndpoint:

        return ApiEndpoint(
            id=model.id,
            api_id=model.api_id,
            method=model.method,
            path=model.path,
            handler=model.handler,
            source_file=(
                Path(model.source_file)
                if model.source_file is not None
                else None
            ),
            line_number=model.line_number,
            summary=model.summary,
            description=model.description,
            tags=model.tags or [],
            version=model.version,
            authentication_required=(
                model.authentication_required
            ),
        )