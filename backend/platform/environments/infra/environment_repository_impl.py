from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.platform.environments.domain.environment import Environment
from backend.platform.environments.infra.environment_model import (
    EnvironmentModel,
)
from backend.platform.environments.repositories.environment_repository import (
    EnvironmentRepository,
)


class EnvironmentRepositoryImpl(EnvironmentRepository):
    """
    SQLAlchemy implementation of the environment repository.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def save(
        self,
        environment: Environment,
    ) -> Environment:
        model = EnvironmentModel(
            id=environment.id,
            project_id=environment.project_id,
            name=environment.name,
            description=environment.description,
            slug=environment.slug,
            environment_type=environment.environment_type,
            created_at=environment.created_at,
            updated_at=environment.updated_at,
        )

        try:
            merged_model = self._session.merge(model)
            self._session.commit()
            self._session.refresh(merged_model)
        
        except:
            self._session.rollback()
            raise

        return self._to_domain(merged_model)

    def get_by_id(
        self,
        environment_id: UUID,
    ) -> Environment | None:
        model = self._session.get(
            EnvironmentModel,
            environment_id,
        )

        if model is None:
            return None

        return self._to_domain(model)

    def list_by_project(
        self,
        project_id: UUID,
    ) -> list[Environment]:
        statement = select(EnvironmentModel).where(
            EnvironmentModel.project_id == project_id,
        )

        models = self._session.scalars(statement).all()

        return [
            self._to_domain(model)
            for model in models
        ]

    def get_by_project_and_slug(
        self,
        project_id: UUID,
        slug: str,
    ) -> Environment | None:
        statement = select(EnvironmentModel).where(
            EnvironmentModel.project_id == project_id,
            EnvironmentModel.slug == slug,
        )

        model = self._session.scalar(statement)

        if model is None:
            return None

        return self._to_domain(model)

    @staticmethod
    def _to_domain(
        model: EnvironmentModel,
    ) -> Environment:
        return Environment(
            id=model.id,
            project_id=model.project_id,
            name=model.name,
            description=model.description,
            slug=model.slug,
            environment_type=model.environment_type,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def delete(
        self,
        environment_id: UUID,
    ) -> None:
        model = self._session.get(
            EnvironmentModel,
            environment_id,
        )

        if model is None:
            return

        try:
            self._session.delete(model)
            self._session.commit()

        except Exception:
            self._session.rollback()
            raise

    def update(
        self,
        environment: Environment,
    ) -> Environment:
        model = self._session.get(
            EnvironmentModel,
            environment.id,
        )

        if model is None:
            raise ValueError(
                "Environment not found",
            )

        model.name = environment.name
        model.description = environment.description
        model.slug = environment.slug
        model.environment_type = environment.environment_type
        model.updated_at = environment.updated_at

        try:
            self._session.commit()
            self._session.refresh(model)

        except Exception:
            self._session.rollback()
            raise

        return self._to_domain(model)