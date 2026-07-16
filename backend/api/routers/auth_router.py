from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from backend.api.dependencies import get_authentication_service
from backend.platform.auth.application.authentication_service import AuthenticationService
from backend.platform.auth.dto.register_user_request import RegisterUserRequest
from backend.platform.auth.dto.user_response import UserResponse
from backend.platform.auth.dto.login_request import LoginRequest
from backend.platform.auth.dto.token_response import TokenResponse
from backend.platform.auth.dto.logout_response import LogoutResponse


router = APIRouter(
    prefix="/auth",
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    request: RegisterUserRequest,
    service: AuthenticationService = Depends(
        get_authentication_service,
    ),
) -> UserResponse:
    """
    Register a new platform user.
    """

    return service.register(request)


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
def login(
    request: LoginRequest,
    service: AuthenticationService = Depends(
        get_authentication_service,
    ),
) -> TokenResponse:
    """
    Authenticate a user and return a JWT access token.
    """

    return service.login(request)


@router.post(
    "/logout",
    response_model=LogoutResponse,
)
def logout() -> LogoutResponse:
    """
    Logout the current user.

    JWT revocation/blacklisting will be implemented
    in a later module.
    """

    return LogoutResponse(
        message="Successfully logged out.",
    )