from pydantic import BaseModel


class ColumnResponse(BaseModel):
    name: str

    data_type: str

    nullable: bool

    default_value: str | None