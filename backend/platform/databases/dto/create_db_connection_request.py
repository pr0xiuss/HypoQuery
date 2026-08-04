from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class CreateDatabaseConnectionRequest(BaseModel):
    """
    Request payload for registering a PostgreSQL database.
    """

    name: str = Field(
        min_length=2,
        max_length=100,
    )

    host: str = Field(
        min_length=1,
        max_length=255,
    )

    port: int = Field(
        ge=1,
        le=65535,
    )

    database_name: str = Field(
        min_length=1,
        max_length=100,
    )

    username: str = Field(
        min_length=1,
        max_length=100,
    )

    password: str = Field(
        min_length=1,
        max_length=255,
    )

    ssl_enabled: bool = False

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )