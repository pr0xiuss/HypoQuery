from pydantic import BaseModel


class ViewSummaryResponse(BaseModel):
    schema: str

    name: str