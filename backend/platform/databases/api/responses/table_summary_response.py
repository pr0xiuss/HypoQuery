from pydantic import BaseModel


class TableSummaryResponse(BaseModel):
    schema: str

    name: str

    estimated_rows: int | None

    size_bytes: int

    column_count: int

    index_count: int

    has_primary_key: bool