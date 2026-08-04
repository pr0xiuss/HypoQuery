from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class ApiError(BaseModel):
    """
    Standard API error model.
    """

    code: str

    message: str

    details: str | None = None

    possible_fix: str | None = None

    documentation: str | None = None

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )


class ErrorResponse(BaseModel):
    """
    Standard failed API response.
    """

    success: bool = Field(default=False)

    error: ApiError

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )