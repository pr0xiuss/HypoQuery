from uuid import UUID

from backend.platform.databases.api.responses.extension_summary_response import ExtensionSummaryResponse
from backend.platform.databases.api.responses.function_summary_response import FunctionSummaryResponse
from backend.platform.databases.api.responses.index_summary_response import IndexSummaryResponse
from backend.platform.databases.api.responses.schema_summary_response import SchemaSummaryResponse
from backend.platform.databases.api.responses.sequence_summary_response import SequenceSummaryResponse
from backend.platform.databases.api.responses.table_detail_response import TableDetailResponse
from backend.platform.databases.api.responses.table_summary_response import TableSummaryResponse
from backend.platform.databases.api.responses.trigger_summary_response import TriggerSummaryResponse
from backend.platform.databases.api.responses.view_summary_response import ViewSummaryResponse
from backend.platform.databases.application.db_explorer_service import DatabaseExplorerService
from backend.platform.databases.repositories.db_metadata_repo import DatabaseMetadataRepository
from backend.platform.databases.api.responses.column_response import ColumnResponse
from backend.platform.databases.api.responses.constraint_response import ConstraintResponse

class DatabaseExplorerServiceImpl(DatabaseExplorerService,):

    def __init__(
        self,
        repository: DatabaseMetadataRepository,
    ) -> None:
        self._repository = repository

    def get_schemas(
        self,
        connection_id: UUID,
    ) -> list[SchemaSummaryResponse]:
        metadata = self._repository.get_by_connection_id(
            connection_id,
        )

        if metadata is None:
            raise ValueError(
                "Database metadata not found.",
            )

        return [
            SchemaSummaryResponse(
                name=schema.name,
                table_count=sum(
                    table.schema_name == schema.name
                    for table in metadata.tables
                ),
                view_count=sum(
                    view.schema_name == schema.name
                    for view in metadata.views
                ),
                function_count=sum(
                    function.schema_name == schema.name
                    for function in metadata.functions
                ),
            )
            for schema in metadata.schemas
        ]

    def get_tables(
        self,
        connection_id: UUID,
    ) -> list[TableSummaryResponse]:
        metadata = self._repository.get_by_connection_id(
            connection_id,
        )

        if metadata is None:
            raise ValueError(
                "Database metadata not found.",
            )

        return [
            TableSummaryResponse(
                schema=table.schema_name,
                name=table.name,
                estimated_rows=table.estimated_rows,
                size_bytes=table.size_bytes,
                column_count=table.column_count,
                index_count=sum(
                    index.table_name == table.name
                    and index.schema_name == table.schema_name
                    for index in metadata.indexes
                ),
                has_primary_key=table.has_primary_key,
            )
            for table in metadata.tables
        ]

    def get_views(
        self,
        connection_id: UUID,
    ) -> list[ViewSummaryResponse]:
        metadata = self._repository.get_by_connection_id(
            connection_id,
        )

        if metadata is None:
            raise ValueError(
                "Database metadata not found.",
            )

        return [
            ViewSummaryResponse(
                schema=view.schema_name,
                name=view.name,
            )
            for view in metadata.views
        ]

    def get_functions(
        self,
        connection_id: UUID,
    ) -> list[FunctionSummaryResponse]:
        metadata = self._repository.get_by_connection_id(
            connection_id,
        )

        if metadata is None:
            raise ValueError(
                "Database metadata not found.",
            )

        return [
            FunctionSummaryResponse(
                schema=function.schema_name,
                name=function.name,
                return_type=function.return_type,
            )
            for function in metadata.functions
        ]

    def get_indexes(
        self,
        connection_id: UUID,
    ) -> list[IndexSummaryResponse]:
        metadata = self._repository.get_by_connection_id(
            connection_id,
        )

        if metadata is None:
            raise ValueError(
                "Database metadata not found.",
            )

        return [
            IndexSummaryResponse(
                schema=index.schema_name,
                table_name=index.table_name,
                name=index.name,
                method=index.method,
                unique=index.unique,
                primary=index.primary,
            )
            for index in metadata.indexes
        ]

    def get_triggers(
        self,
        connection_id: UUID,
    ) -> list[TriggerSummaryResponse]:
        metadata = self._repository.get_by_connection_id(
            connection_id,
        )

        if metadata is None:
            raise ValueError(
                "Database metadata not found.",
            )

        return [
            TriggerSummaryResponse(
                schema=trigger.schema_name,
                table_name=trigger.table_name,
                name=trigger.name,
                event=trigger.event,
                timing=trigger.timing,
            )
            for trigger in metadata.triggers
        ]

    def get_sequences(
        self,
        connection_id: UUID,
    ) -> list[SequenceSummaryResponse]:
        metadata = self._repository.get_by_connection_id(
            connection_id,
        )

        if metadata is None:
            raise ValueError(
                "Database metadata not found.",
            )

        return [
            SequenceSummaryResponse(
                schema=sequence.schema_name,
                name=sequence.name,
            )
            for sequence in metadata.sequences
        ]

    def get_extensions(
        self,
        connection_id: UUID,
    ) -> list[ExtensionSummaryResponse]:
        metadata = self._repository.get_by_connection_id(
            connection_id,
        )

        if metadata is None:
            raise ValueError(
                "Database metadata not found.",
            )

        return [
            ExtensionSummaryResponse(
                name=extension.name,
                version=extension.version,
            )
            for extension in metadata.extensions
        ]

    def get_table(
        self,
        connection_id: UUID,
        schema_name: str,
        table_name: str,
    ) -> TableDetailResponse:
        metadata = self._repository.get_by_connection_id(
            connection_id,
        )

        if metadata is None:
            raise ValueError(
                "Database metadata not found.",
            )

        table = next(
            (
                table
                for table in metadata.tables
                if table.schema_name == schema_name
                and table.name == table_name
            ),
            None,
        )

        if table is None:
            raise ValueError(
                "Table not found.",
            )

        print(metadata.constraints)

        return TableDetailResponse(
            schema=table.schema_name,
            name=table.name,
            estimated_rows=None,
            size_bytes=None,
            columns=[
                ColumnResponse(
                    name=column.name,
                    data_type=column.data_type,
                    nullable=column.nullable,
                    default_value=column.default_value,
                )
                for column in metadata.columns
                if column.schema_name == schema_name
                and column.table_name == table_name
            ],
            constraints=[
                ConstraintResponse(
                    name=constraint.name,
                    constraint_type=constraint.constraint_type,
                    definition="",
                )
                for constraint in metadata.constraints
                if constraint.schema_name == schema_name
                and constraint.table_name == table_name
            ],
            indexes=[
                IndexSummaryResponse(
                    schema=index.schema_name,
                    table_name=index.table_name,
                    name=index.name,
                    method=index.method,
                    unique=index.unique,
                    primary=index.primary,
                )
                for index in metadata.indexes
                if index.schema_name == schema_name
                and index.table_name == table_name
            ],
        )