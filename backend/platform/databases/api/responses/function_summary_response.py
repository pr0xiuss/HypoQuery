from pydantic import BaseModel


class FunctionSummaryResponse(BaseModel):
    schema: str

    name: str

    return_type: str | None