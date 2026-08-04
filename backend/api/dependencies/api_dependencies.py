from backend.platform.apis.service.api_service import ApiService
from backend.platform.apis.application.api_service_impl import ApiServiceImpl
from backend.platform.apis.infra.sqlalchemy_api_repo import SqlAlchemyApiRepository
from backend.platform.apis.repositories.api_repo import ApiRepository
from fastapi import Depends
from sqlalchemy.orm import Session
from backend.platform.databases.repositories.db_metadata_repo_impl import DatabaseMetadataRepositoryImpl
from backend.platform.databases.application.db_explorer_service import DatabaseExplorerService
from backend.platform.databases.application.db_explorer_service_impl import DatabaseExplorerServiceImpl
from backend.platform.shared.database import get_db_session


def get_api_repository(
    session: Session = Depends(
        get_db_session,
    ),
) -> ApiRepository:
    return SqlAlchemyApiRepository(
        session,
    )


def get_api_service(
    session: Session = Depends(
        get_db_session,
    ),
) -> ApiService:
    repository = SqlAlchemyApiRepository(
        session,
    )

    return ApiServiceImpl(
        repository=repository,
    )

def get_database_explorer_service(
    session: Session = Depends(
        get_db_session,
    ),
) -> DatabaseExplorerService:
    repository = DatabaseMetadataRepositoryImpl(
        session,
    )

    return DatabaseExplorerServiceImpl(
        repository=repository,
    )