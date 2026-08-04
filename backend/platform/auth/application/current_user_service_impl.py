from uuid import UUID

from backend.platform.auth.application.current_user_service import CurrentUserService
from backend.platform.auth.domain.user import User
from backend.platform.auth.repositories.user_repository import UserRepository
from backend.platform.shared.exceptions import ResourceNotFoundError

class CurrentUserServiceImpl(CurrentUserService):
    """
    Default implementation for resolving the authenticated user.
    """

    def __init__(
        self,
        user_repository: UserRepository,
    ) -> None:
        self._user_repository = user_repository

    def get_current_user(
        self,
        user_id: UUID,
    ) -> User:
        user = self._user_repository.get_by_id(
            user_id,
        )

        if user is None:
            raise ResourceNotFoundError(
                "User not found.",
                user_id
            )

        return user