from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr
from pydantic import Field


class RegisterUserRequest(BaseModel):
    """
    Request payload for user registration.
    """

    username: str = Field(
        min_length=3,
        max_length=50,
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128,
    )

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )