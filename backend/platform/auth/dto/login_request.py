from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class LoginRequest(BaseModel):
    """
    Request DTO for user login.

    The identifier may be either the username or email.
    """

    identifier: str = Field(
        min_length=3,
        max_length=255,
        description="Username or email address.",
    )

    password: str = Field(
        min_length=8,
        description="User password.",
    )

    model_config = ConfigDict(
        frozen=True,
    )