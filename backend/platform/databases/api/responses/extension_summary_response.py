from pydantic import BaseModel


class ExtensionSummaryResponse(BaseModel):
    name: str

    version: str