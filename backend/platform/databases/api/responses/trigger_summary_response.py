from pydantic import BaseModel


class TriggerSummaryResponse(BaseModel):
    schema: str

    table_name: str

    name: str

    event: str

    timing: str