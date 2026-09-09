from unittest.mock import Mock
from uuid import uuid4

from backend.platform.auth.application.current_user_service_impl import (
    CurrentUserServiceImpl,
)
from backend.platform.auth.domain.user import User
from tests.factories import create_user

def test_get_current_user():
    """
    Existing users are returned successfully.
    """

    repository = Mock()

    user = create_user()

    repository.get_by_id.return_value = user

    service = CurrentUserServiceImpl(
        repository,
    )

    result = service.get_current_user(
        user.id,
    )

    assert result == user