from unittest.mock import Mock
from uuid import uuid4

import pytest

from backend.platform.auth.application.current_user_service_impl import (
    CurrentUserServiceImpl,
)
from backend.platform.shared.exceptions import (
    ResourceNotFoundError,
)


def test_missing_user():
    """
    Missing users raise ResourceNotFoundError.
    """

    repository = Mock()

    repository.get_by_id.return_value = None

    service = CurrentUserServiceImpl(
        repository,
    )

    with pytest.raises(
        ResourceNotFoundError,
    ):
        service.get_current_user(
            uuid4(),
        )