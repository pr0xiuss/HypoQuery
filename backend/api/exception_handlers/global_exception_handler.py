from fastapi import Request
from fastapi.responses import JSONResponse

from backend.platform.shared.dto.api_error import ApiError
from backend.platform.shared.dto.api_error import ErrorResponse
from backend.shared.logger import get_logger


logger = get_logger(__name__)


async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """
    Global fallback exception handler.

    Any unexpected exception reaching this handler is treated as an
    internal server error. Details are logged while a standardized
    error response is returned to the client.
    """

    logger.exception(
        "Unhandled exception while processing request %s %s",
        request.method,
        request.url.path,
    )

    response = ErrorResponse(
        error=ApiError(
            code="INTERNAL_SERVER_ERROR",
            message="An unexpected error occurred.",
            details="Please contact the administrator if the problem persists.",
        )
    )

    return JSONResponse(
        status_code=500,
        content=response.model_dump(),
    )