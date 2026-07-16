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

    def exists_by_name(
        self,
        project_id: UUID,
        name: str,
    ) -> bool:
        statement = select(EnvironmentModel).where(
            EnvironmentModel.project_id == project_id,
            EnvironmentModel.name == name,
        )

        return self._session.scalar(statement) is not None

    @staticmethod
    def _to_domain(
        model: EnvironmentModel,
    ) -> Environment:
        return Environment(
            id=model.id,
            project_id=model.project_id,
            name=model.name,
            description=model.description,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )