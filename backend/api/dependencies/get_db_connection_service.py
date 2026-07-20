from sqlalchemy.orm import Session

from backend.platform.shared.database import get_db_session
from backend.platform.databases.application.db_connection_service import (
    DatabaseConnectionService,
)
from backend.platform.databases.application.db_connection_service_impl import (
    DatabaseConnectionServiceImpl,
)
from backend.platform.databases.infra.db_connection_repo_impl import (
    DatabaseConnectionRepositoryImpl,
)
from fastapi import Depends


def get_database_connection_service(
    session: Session = Depends(
        get_db_session,
    ),
) -> DatabaseConnectionService:
    """
    Dependency provider for the database connection service.
    """

    repository = DatabaseConnectionRepositoryImpl(
        session,
    )

    return DatabaseConnectionServiceImpl(
        repository,
    )