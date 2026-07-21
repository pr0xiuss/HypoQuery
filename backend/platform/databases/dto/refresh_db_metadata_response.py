from pydantic import BaseModel


class RefreshDatabaseMetadataResponse(BaseModel):
    message: str