from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class TokenResponse(BaseModel):
    """
    Response DTO containing JWT tokens.
    """

    access_token: str = Field(
        description="JWT access token.",
    )

    token_type: str = Field(
        default="Bearer",
        description="Authentication scheme.",
    )

    expires_in: int = Field(
        description="Access token lifetime in seconds.",
    )

    model_config = ConfigDict(
        frozen=True,
    )