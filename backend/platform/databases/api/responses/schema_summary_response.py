from pydantic import BaseModel


class SchemaSummaryResponse(BaseModel):
    name: str

    table_count: int

    view_count: int

    function_count: int