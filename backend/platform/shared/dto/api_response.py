from typing import Generic
from typing import TypeVar, Any

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


    @classmethod
    def success_response(
        cls,
        data: T | None = None,
        meta: dict[str, object] | None = None,
    ) -> "ApiResponse[T]":
        """
        Creates a successful API response.
        """

        return cls(
            success=True,
            data=data,
            meta=meta or {},
            errors=[],
        )

    @classmethod
    def failure(
        cls,
        error: Any,
        meta: dict[str, object] | None = None,
    ) -> "ApiResponse[None]":
        """
        Creates a failed API response.
        """

        return cls(
            success=False,
            data=None,
            meta=meta or {},
            errors=[error],
        )