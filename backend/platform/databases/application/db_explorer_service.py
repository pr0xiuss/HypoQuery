from abc import ABC
from abc import abstractmethod
from uuid import UUID

from backend.platform.databases.api.responses.extension_summary_response import (
    ExtensionSummaryResponse,
)
from backend.platform.databases.api.responses.function_summary_response import (
    FunctionSummaryResponse,
)
from backend.platform.databases.api.responses.index_summary_response import (
    IndexSummaryResponse,
)
from backend.platform.databases.api.responses.schema_summary_response import (
    SchemaSummaryResponse,
)
from backend.platform.databases.api.responses.sequence_summary_response import (
    SequenceSummaryResponse,
)
from backend.platform.databases.api.responses.table_detail_response import (
    TableDetailResponse,
)
from backend.platform.databases.api.responses.table_summary_response import (
    TableSummaryResponse,
)
from backend.platform.databases.api.responses.trigger_summary_response import (
    TriggerSummaryResponse,
)
from backend.platform.databases.api.responses.view_summary_response import (
    ViewSummaryResponse,
)


class DatabaseExplorerService(ABC):
    @abstractmethod
    def get_schemas(
        self,
        connection_id: UUID,
    ) -> list[SchemaSummaryResponse]:
        pass

    @abstractmethod
    def get_tables(
        self,
        connection_id: UUID,
    ) -> list[TableSummaryResponse]:
        pass

    @abstractmethod
    def get_table(
        self,
        connection_id: UUID,
        schema_name: str,
        table_name: str,
    ) -> TableDetailResponse:
        pass

    @abstractmethod
    def get_views(
        self,
        connection_id: UUID,
    ) -> list[ViewSummaryResponse]:
        pass

    @abstractmethod
    def get_functions(
        self,
        connection_id: UUID,
    ) -> list[FunctionSummaryResponse]:
        pass

    @abstractmethod
    def get_indexes(
        self,
        connection_id: UUID,
    ) -> list[IndexSummaryResponse]:
        pass

    @abstractmethod
    def get_triggers(
        self,
        connection_id: UUID,
    ) -> list[TriggerSummaryResponse]:
        pass

    @abstractmethod
    def get_sequences(
        self,
        connection_id: UUID,
    ) -> list[SequenceSummaryResponse]:
        pass

    @abstractmethod
    def get_extensions(
        self,
        connection_id: UUID,
    ) -> list[ExtensionSummaryResponse]:
        pass