from typing import Generic
from typing import TypeVar

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """
    Standard successful API response.
    """

    success: bool = Field(default=True)

    data: T | None = None

    meta: dict[str, object] = Field(default_factory=dict)

    errors: list[object] = Field(default_factory=list)

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )