from abc import ABC
from abc import abstractmethod
from backend.platform.auth.dto.logout_response import LogoutResponse
from backend.platform.auth.dto.refresh_token_response import RefreshTokenResponse
from backend.platform.auth.dto.register_user_request import RegisterUserRequest
from backend.platform.auth.dto.user_response import UserResponse
from backend.platform.auth.dto.login_request import LoginRequest
from backend.platform.auth.dto.token_response import TokenResponse

class AuthenticationService(ABC):
    """
    Application service responsible for user authentication workflows.
    """

    @abstractmethod
    def register(
        self,
        request: RegisterUserRequest,
    ) -> UserResponse:
        """
        Register a new platform user.
        """
        raise NotImplementedError
        
    @abstractmethod
    def login(
        self,
        request: LoginRequest,
    ) -> TokenResponse:
        """
        Authenticate a user and return JWT tokens.
        """
        raise NotImplementedError
    
    @abstractmethod
    def refresh_token(
        self,
        refresh_token: str,
    ) -> RefreshTokenResponse:
        """
        Generates a new access token using a refresh token.
        """
        raise NotImplementedError

    @abstractmethod
    def logout(
        self,
    ) -> LogoutResponse:
        """
        Logs out the current user.
        """
        raise NotImplementedError