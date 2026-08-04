from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.platform.databases.domain.db_connection import DatabaseConnection
from backend.platform.databases.infra.db_connection_model import DatabaseConnectionModel
from backend.platform.databases.repositories.db_connection_repo import DatabaseConnectionRepository
from backend.platform.shared.exceptions.resource import ResourceNotFoundError

class DatabaseConnectionRepositoryImpl(
    DatabaseConnectionRepository,
):
    """
    SQLAlchemy implementation of the database connection repository.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def save(
        self,
        connection: DatabaseConnection,
    ) -> DatabaseConnection:
        model = DatabaseConnectionModel(
            id=connection.id,
            environment_id=connection.environment_id,
            password=connection.password,
            name=connection.name,
            host=connection.host,
            port=connection.port,
            database_name=connection.database_name,
            username=connection.username,
            ssl_enabled=connection.ssl_enabled,
            is_active=connection.is_active,
            created_at=connection.created_at,
            updated_at=connection.updated_at,
        )

        try:
            merged_model = self._session.merge(
                model,
            )
            self._session.commit()
            self._session.refresh(
                merged_model,
            )

        except:
            self._session.rollback()
            raise

        return self._to_domain(
            merged_model,
        )

    def get_by_id(
        self,
        connection_id: UUID,
    ) -> DatabaseConnection | None:
        model = self._session.get(
            DatabaseConnectionModel,
            connection_id,
        )
        if model is None:
            return None

        return self._to_domain(model)
    

    def list_by_environment(
        self,
        environment_id: UUID,
    ) -> list[DatabaseConnection]:
        statement = select(
            DatabaseConnectionModel,
        ).where(
            DatabaseConnectionModel.environment_id == environment_id,
        )

        models = self._session.scalars(
            statement,
        ).all()

        return [
            self._to_domain(
                model,
            )
            for model in models
        ]

    def delete(
        self,
        connection_id: UUID,
    ) -> None:
        model = self._session.get(
            DatabaseConnectionModel,
            connection_id,
        )

        if model is None:
            raise ResourceNotFoundError("Database Connection", str(connection_id))
        try:
            self._session.delete(
                model,
            )
            self._session.commit()

        except:
            self._session.rollback()
            raise

    def update(
        self,
        connection: DatabaseConnection,
    ) -> DatabaseConnection:
        model = self._session.get(
            DatabaseConnectionModel,
            connection.id,
        )

        if model is None:
            raise ResourceNotFoundError(
                "Database Connection",
                str(connection.id),
            )

        model.name = connection.name
        model.host = connection.host
        model.port = connection.port
        model.database_name = connection.database_name
        model.username = connection.username
        model.password = connection.password
        model.ssl_enabled = connection.ssl_enabled
        model.is_active = connection.is_active
        model.updated_at = connection.updated_at

        try:
            self._session.commit()
            self._session.refresh(
                model,
            )

        except:
            self._session.rollback()
            raise

        return self._to_domain(
            model,
        )

    @staticmethod
    def _to_domain(
        model: DatabaseConnectionModel,
    ) -> DatabaseConnection:
        return DatabaseConnection(
            id=model.id,
            environment_id=model.environment_id,
            password=model.password,
            name=model.name,
            host=model.host,
            port=model.port,
            database_name=model.database_name,
            username=model.username,
            ssl_enabled=model.ssl_enabled,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

