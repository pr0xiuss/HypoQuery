from uuid import UUID

from sqlalchemy.orm import Session
from dataclasses import asdict
from backend.platform.databases.domain.db_metadata import DatabaseMetadata
from backend.platform.databases.dto.db_statistics_result import DatabaseStatisticsResult
from backend.platform.databases.infra.db_metadata_model import DatabaseMetadataModel
from backend.platform.databases.repositories.db_metadata_repo import DatabaseMetadataRepository
from backend.platform.databases.domain.db_extension import DatabaseExtension
from backend.platform.databases.domain.db_sequence import DatabaseSequence
from backend.platform.databases.domain.db_trigger import DatabaseTrigger
from backend.platform.databases.domain.db_index import DatabaseIndex
from backend.platform.databases.domain.db_function import DatabaseFunction
from backend.platform.databases.domain.db_schema import DatabaseSchema
from backend.platform.databases.domain.db_view import DatabaseView
from backend.platform.databases.domain.db_table import DatabaseTable
from backend.platform.databases.domain.db_column import DatabaseColumn
from backend.platform.databases.domain.db_constraint import DatabaseConstraint

class DatabaseMetadataRepositoryImpl(
    DatabaseMetadataRepository,
):
    def __init__(
        self,
        session: Session,
    ):
        self._session = session

    def _serialize(self, obj):
        data = asdict(obj)
        data["id"] = str(data["id"])
        data["connection_id"] = str(data["connection_id"])
        return data

    def save(
        self,
        metadata: DatabaseMetadata,
    ) -> DatabaseMetadata:
        print(metadata.indexes[0])
        print(self._serialize(metadata.indexes[0]))
        model = DatabaseMetadataModel(
            id=str(metadata.id),
            connection_id=str(metadata.connection_id),
            postgres_version=metadata.postgres_version,
            database_size=metadata.database_size,
            settings=metadata.settings,
            replication=metadata.replication,
            database_statistics=metadata.database_statistics.model_dump(),
            table_statistics=metadata.table_statistics,
            index_statistics=metadata.index_statistics,
            connection_statistics=metadata.connection_statistics,
            lock_statistics=metadata.lock_statistics,
            schemas=[self._serialize(schema) for schema in metadata.schemas],
            tables=[self._serialize(table) for table in metadata.tables],
            columns=[self._serialize(column) for column in metadata.columns],
            constraints=[self._serialize(constraint) for constraint in metadata.constraints],
            views=[self._serialize(view) for view in metadata.views],
            functions=[self._serialize(function) for function in metadata.functions],
            indexes=[self._serialize(index) for index in metadata.indexes],
            triggers=[self._serialize(trigger) for trigger in metadata.triggers],
            sequences=[self._serialize(sequence) for sequence in metadata.sequences],
            extensions=[self._serialize(extension) for extension in metadata.extensions],
            last_refreshed=metadata.last_refreshed,
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
            id=model.id,
            connection_id=model.connection_id,
            postgres_version=model.postgres_version,
            database_size=model.database_size,
            settings=model.settings,
            replication=model.replication,
            database_statistics=DatabaseStatisticsResult.model_validate(
                model.database_statistics,
            ),
            table_statistics=model.table_statistics,
            index_statistics=model.index_statistics,
            connection_statistics=model.connection_statistics,
            lock_statistics=model.lock_statistics,
            schemas=[
                DatabaseSchema(
                    id=UUID(schema["id"]),
                    connection_id=UUID(schema["connection_id"]),
                    name=schema["name"],
                )
                for schema in model.schemas
            ],
            tables=[
                DatabaseTable(
                    id=UUID(table["id"]),
                    connection_id=UUID(table["connection_id"]),
                    schema_name=table["schema_name"],
                    name=table["name"],
                    estimated_rows=table["estimated_rows"],
                    size_bytes=table["size_bytes"],
                    column_count=table["column_count"],
                    has_primary_key=table["has_primary_key"],
                )
                for table in model.tables
            ],
            columns=[
                DatabaseColumn(
                    id=UUID(column["id"]),
                    connection_id=UUID(column["connection_id"]),
                    schema_name=column["schema_name"],
                    table_name=column["table_name"],
                    name=column["name"],
                    data_type=column["data_type"],
                    nullable=column["nullable"],
                    default_value=column["default_value"],
                    ordinal_position=column["ordinal_position"],
                )
                for column in model.columns
            ],
            constraints=[
                DatabaseConstraint(
                    id=UUID(constraint["id"]),
                    connection_id=UUID(constraint["connection_id"]),
                    schema_name=constraint["schema_name"],
                    table_name=constraint["table_name"],
                    name=constraint["name"],
                    constraint_type=constraint["constraint_type"],
                )
                for constraint in (model.constraints or [])
            ],
            views=[
                DatabaseView(
                    id=UUID(view["id"]),
                    connection_id=UUID(view["connection_id"]),
                    schema_name=view["schema_name"],
                    name=view["name"],
                )
                for view in model.views
            ],
            functions=[
                DatabaseFunction(
                    id=UUID(function["id"]),
                    connection_id=UUID(function["connection_id"]),
                    schema_name=function["schema_name"],
                    name=function["name"],
                    return_type=function["return_type"],
                )
                for function in model.functions
            ],
            indexes=[
                DatabaseIndex(
                    id=UUID(index["id"]),
                    connection_id=UUID(index["connection_id"]),
                    schema_name=index["schema_name"],
                    table_name=index["table_name"],
                    name=index["name"],
                    method=index["method"],
                    unique=index["unique"],
                    primary=index["primary"],
                )
                for index in model.indexes
            ],
            triggers=[
                DatabaseTrigger(
                    id=UUID(trigger["id"]),
                    connection_id=UUID(trigger["connection_id"]),
                    schema_name=trigger["schema_name"],
                    table_name=trigger["table_name"],
                    name=trigger["name"],
                    event=trigger["event"],
                    timing=trigger["timing"],
                )
                for trigger in model.triggers
            ],
            sequences=[
                DatabaseSequence(
                    id=UUID(sequence["id"]),
                    connection_id=UUID(sequence["connection_id"]),
                    schema_name=sequence["schema_name"],
                    name=sequence["name"],
                )
                for sequence in model.sequences
            ],
            extensions=[
                DatabaseExtension(
                    id=UUID(extension["id"]),
                    connection_id=UUID(extension["connection_id"]),
                    name=extension["name"],
                    version=extension["version"],
                )
                for extension in model.extensions
            ],
            last_refreshed=model.last_refreshed,
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