from abc import ABC
from abc import abstractmethod
from uuid import UUID


class JWTService(ABC):
    """
    Contract for JWT token generation and validation.
    """

    @abstractmethod
    def create_access_token(
        self,
        user_id: UUID,
    ) -> str:
        """
        Creates an access token.
        """
        raise NotImplementedError

    @abstractmethod
    def verify_access_token(
        self,
        token: str,
    ) -> UUID:
        """
        Verifies an access token and returns the user id.
        """
        raise NotImplementedError