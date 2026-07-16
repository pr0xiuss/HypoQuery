from abc import ABC
from abc import abstractmethod


class PasswordHasher(ABC):
    """
    Contract for password hashing.
    """

    @abstractmethod
    def hash(
        self,
        password: str,
    ) -> str:
        """
        Hash a plain-text password.
        """
        raise NotImplementedError

    @abstractmethod
    def verify(
        self,
        password: str,
        password_hash: str,
    ) -> bool:
        """
        Verify a plain-text password against a hash.
        """
        raise NotImplementedError