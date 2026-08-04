from abc import ABC
from abc import abstractmethod
from uuid import UUID

from backend.platform.auth.domain.user import User


class CurrentUserService(ABC):
    """
    Resolves the currently authenticated user.
    """

    @abstractmethod
    def get_current_user(
        self,
        user_id: UUID,
    ) -> User:
        """
        Returns the currently authenticated user.
        """
        raise NotImplementedError