from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class RefreshTokenRequest(BaseModel):
    """
    Request payload for refreshing an access token.
    """

    refresh_token: str = Field(
        min_length=1,
    )

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )