from uuid import UUID

from sqlalchemy.orm import Session

from backend.platform.databases.domain.db_metadata import (
    DatabaseMetadata,
)
from backend.platform.databases.infra.db_metadata_model import (
    DatabaseMetadataModel,
)
from backend.platform.databases.repositories.db_metadata_repo import (
    DatabaseMetadataRepository,
)


class DatabaseMetadataRepositoryImpl(
    DatabaseMetadataRepository,
):
    def __init__(
        self,
        session: Session,
    ):
        self._session = session

    def save(
        self,
        metadata: DatabaseMetadata,
    ) -> DatabaseMetadata:
        model = DatabaseMetadataModel(
            id=str(metadata.id),
            connection_id=str(metadata.connection_id),
            postgres_version=metadata.postgres_version,
            schemas=metadata.schemas,
            tables=metadata.tables,
            views=metadata.views,
            functions=metadata.functions,
            indexes=metadata.indexes,
            triggers=metadata.triggers,
            sequences=metadata.sequences,
            extensions=metadata.extensions,
        )

        self._session.merge(model)
        self._session.commit()

        return metadata

    def get_by_connection_id(
        self,
        connection_id: UUID,
    ) -> DatabaseMetadata | None:
        model = (
            self._session.query(
                DatabaseMetadataModel,
            )
            .filter_by(
                connection_id=str(connection_id),
            )
            .first()
        )

        if model is None:
            return None

        return DatabaseMetadata(
            id=UUID(model.id),
            connection_id=UUID(model.connection_id),
            postgres_version=model.postgres_version,
            schemas=model.schemas,
            tables=model.tables,
            views=model.views,
            functions=model.functions,
            indexes=model.indexes,
            triggers=model.triggers,
            sequences=model.sequences,
            extensions=model.extensions,
        )

    def delete_by_connection_id(
        self,
        connection_id: UUID,
    ) -> None:
        (
            self._session.query(
                DatabaseMetadataModel,
            )
            .filter_by(
                connection_id=str(connection_id),
            )
            .delete()
        )

        self._session.commit()