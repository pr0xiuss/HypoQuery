from pydantic import BaseModel


class SequenceSummaryResponse(BaseModel):
    schema: str

    name: str