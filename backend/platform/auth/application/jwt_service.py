from abc import ABC
from abc import abstractmethod
from uuid import UUID


class JWTService(ABC):
    """
    Service responsible for issuing and validating JWTs.
    """

    @abstractmethod
    def create_access_token(
        self,
        user_id: UUID,
    ) -> str:
        """
        Creates an access token.
        """

    @abstractmethod
    def create_refresh_token(
        self,
        user_id: UUID,
    ) -> str:
        """
        Creates a refresh token.
        """

    @abstractmethod
    def verify_access_token(
        self,
        token: str,
    ) -> UUID:
        """
        Returns the authenticated user id.
        """

    @abstractmethod
    def verify_refresh_token(
        self,
        token: str,
    ) -> UUID:
        """
        Returns the authenticated user id.
        """

    @abstractmethod
    def access_token_expires_in(
        self,
    ) -> int:
        """
        Access token lifetime in seconds.
        """