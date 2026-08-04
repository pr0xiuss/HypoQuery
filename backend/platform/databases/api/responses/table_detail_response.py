from pydantic import BaseModel

from backend.platform.databases.api.responses.column_response import ColumnResponse
from backend.platform.databases.api.responses.constraint_response import ConstraintResponse
from backend.platform.databases.api.responses.index_summary_response import IndexSummaryResponse
from backend.platform.databases.api.responses.constraint_response import ConstraintResponse


class TableDetailResponse(BaseModel):
    schema: str

    name: str

    estimated_rows: int | None

    size_bytes: int | None

    columns: list[ColumnResponse]

    constraints: list[ConstraintResponse]

    indexes: list[IndexSummaryResponse]