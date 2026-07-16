from datetime import datetime, UTC
from uuid import uuid4

from backend.platform.auth.application.authentication_service import (
    AuthenticationService,
)
from backend.platform.auth.domain.user import User
from backend.platform.auth.dto.register_user_request import (
    RegisterUserRequest,
)
from backend.platform.auth.dto.user_response import UserResponse
from backend.platform.auth.repositories.user_repository import UserRepository
from backend.platform.auth.application.password_hasher import (
    PasswordHasher,
)
from backend.platform.auth.dto.login_request import LoginRequest
from backend.platform.auth.dto.token_response import TokenResponse
from backend.platform.auth.application.jwt_service import JWTService
from backend.platform.shared.exceptions import (
    AccountDisabledError,
    InvalidCredentialsError,
    UserAlreadyExistsError,
    UserNotVerifiedError,
)


class AuthenticationServiceImpl(AuthenticationService):
    """
    Default implementation of the authentication application service.
    """

    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        jwt_service: JWTService,
    ) -> None:
        self._user_repository = user_repository
        self._password_hasher = password_hasher
        self._jwt_service = jwt_service

    def register(
        self,
        request: RegisterUserRequest,
    ) -> UserResponse:
        now = datetime.now(UTC)

        existing_user = self._user_repository.get_by_identifier(
            request.username,
        )

        if existing_user is None:
            existing_user = self._user_repository.get_by_identifier(
                request.email,
            )

        if existing_user is not None:
            raise UserAlreadyExistsError(
                "A user with this username or email already exists."
            )

        password_hash = self._password_hasher.hash(
            request.password,
        )

        user = User(
            id=uuid4(),
            username=request.username,
            email=request.email,
            password_hash=password_hash,
            is_active=True, 
            is_verified=False,
            created_at=now,
            updated_at=now,
        )

        persisted_user = self._user_repository.save(user)

        return UserResponse(
            id=persisted_user.id,
            username=persisted_user.username,
            email=persisted_user.email,
            is_active=persisted_user.is_active,
            is_verified=persisted_user.is_verified,
            created_at=persisted_user.created_at,
            updated_at=persisted_user.updated_at,
        )
    
    def login(
        self,
        request: LoginRequest,
    ) -> TokenResponse:
        user = self._user_repository.get_by_identifier(
            request.identifier,
        )

        if user is None:
            raise InvalidCredentialsError(
                "Invalid username/email or password.",
            )

        if not self._password_hasher.verify(
            request.password,
            user.password_hash,
        ):
            raise InvalidCredentialsError(
                "Invalid username/email or password.",
            )
        
        if not user.is_active:
            raise AccountDisabledError(
                "This account has been disabled.",
            )

        if not user.is_verified:
            raise UserNotVerifiedError(
                "Please verify your email before logging in.",
            )

        access_token = self._jwt_service.create_access_token(
            user.id,
        )

        return TokenResponse(
            access_token=access_token,
            expires_in=3600,
        )