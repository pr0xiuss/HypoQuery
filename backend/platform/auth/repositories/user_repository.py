from abc import ABC
from abc import abstractmethod
from uuid import UUID

from backend.platform.auth.domain.user import User


class UserRepository(ABC):
    """
    Repository contract for user persistence.
    """

    @abstractmethod
    def save(
        self,
        user: User,
    ) -> User:
        """
        Persist a user.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_id(
        self,
        user_id: UUID,
    ) -> User | None:
        """
        Retrieve a user by its identifier.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_email(
        self,
        email: str,
    ) -> User | None:
        """
        Retrieve a user by email.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_username(
        self,
        username: str,
    ) -> User | None:
        """
        Retrieve a user by username.
        """
        raise NotImplementedError
    
    @abstractmethod
    def get_by_identifier(
        self,
        identifier: str,
    ) -> User | None:
        """
        Returns a user by username or email.
        """
        raise NotImplementedError