from pydantic import BaseModel
from pydantic import ConfigDict


class RefreshTokenResponse(BaseModel):
    """
    Response returned after refreshing an access token.
    """

    access_token: str

    token_type: str = "Bearer"

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )