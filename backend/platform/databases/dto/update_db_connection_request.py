from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class UpdateDatabaseConnectionRequest(BaseModel):
    """
    Request payload for updating a PostgreSQL database connection.
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