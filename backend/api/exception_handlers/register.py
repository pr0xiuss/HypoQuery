from fastapi import FastAPI

from backend.api.exception_handlers.global_exception_handler import (
    authentication_exception_handler,
    authorization_exception_handler,
    resource_exception_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)
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


def register_exception_handlers(
    app: FastAPI,
) -> None:
    """
    Registers all application exception handlers.
    """

    app.add_exception_handler(
        InvalidCredentialsError,
        authentication_exception_handler,
    )

    app.add_exception_handler(
        UserNotVerifiedError,
        authentication_exception_handler,
    )

    app.add_exception_handler(
        AccountDisabledError,
        authentication_exception_handler,
    )

    app.add_exception_handler(
        PermissionDeniedError,
        authorization_exception_handler,
    )

    app.add_exception_handler(
        ResourceNotFoundError,
        resource_exception_handler,
    )

    app.add_exception_handler(
        ResourceAlreadyExistsError,
        resource_exception_handler,
    )

    app.add_exception_handler(
        UserAlreadyExistsError,
        resource_exception_handler,
    )

    app.add_exception_handler(
        ValidationError,
        validation_exception_handler,
    )

    app.add_exception_handler(
        Exception,
        unhandled_exception_handler,
    )