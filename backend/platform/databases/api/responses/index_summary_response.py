from pydantic import BaseModel


class IndexSummaryResponse(BaseModel):
    schema: str

    table_name: str

    name: str

    method: str

    unique: bool

    primary: bool