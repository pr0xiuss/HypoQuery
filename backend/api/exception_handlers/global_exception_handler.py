from fastapi import Request
from fastapi.responses import JSONResponse
import backend.platform.shared.dto.api_error
import backend.platform.shared.dto.api_response
from backend.platform.shared.dto.api_error import ApiError
from backend.platform.shared.dto.api_error import ErrorResponse
from backend.shared.logger import get_logger
from backend.platform.shared.exceptions import (
    AccountDisabledError,
    InvalidCredentialsError,
    PermissionDeniedError,
    ResourceAlreadyExistsError,
    ResourceNotFoundError,
    UserAlreadyExistsError,
    UserNotVerifiedError,
    ValidationError,
)


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


async def authentication_exception_handler(
    request: Request,
    exc: (
        InvalidCredentialsError
        | UserNotVerifiedError
        | AccountDisabledError
    ),
) -> JSONResponse:
    """
    Handles authentication-related exceptions.
    """

    response = backend.platform.shared.dto.api_response.ApiResponse.failure(
        error=backend.platform.shared.dto.api_error.ApiError(
            code=exc.__class__.__name__,
            message=str(exc),
        ),
    )

    return JSONResponse(
        status_code=401,
        content=response.model_dump(mode="json"),
    )


async def authorization_exception_handler(
    request: Request,
    exc: PermissionDeniedError,
) -> JSONResponse:
    """
    Handles authorization failures.
    """

    response = backend.platform.shared.dto.api_response.ApiResponse.failure(
        error=backend.platform.shared.dto.api_error.ApiError(
            code=exc.__class__.__name__,
            message=str(exc),
        ),
    )

    return JSONResponse(
        status_code=403,
        content=response.model_dump(mode="json"),
    )


async def resource_exception_handler(
    request: Request,
    exc: (
        ResourceNotFoundError
        | ResourceAlreadyExistsError
        | UserAlreadyExistsError
    ),
) -> JSONResponse:
    """
    Handles resource-related exceptions.
    """

    status_code = (
        404
        if isinstance(exc, ResourceNotFoundError)
        else 409
    )

    response = backend.platform.shared.dto.api_response.ApiResponse.failure(
        error=backend.platform.shared.dto.api_error.ApiError(
            code=exc.__class__.__name__,
            message=str(exc),
        ),
    )

    return JSONResponse(
        status_code=status_code,
        content=response.model_dump(mode="json"),
    )


async def validation_exception_handler(
    request: Request,
    exc: ValidationError,
) -> JSONResponse:
    """ 
    Handles business validation failures.
    """

    response = backend.platform.shared.dto.api_response.ApiResponse.failure(
        error=backend.platform.shared.dto.api_error.ApiError(
            code=exc.__class__.__name__,
            message=str(exc),
        ),
    )

    return JSONResponse(
        status_code=400,
        content=response.model_dump(mode="json"),
    )