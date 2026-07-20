from unittest.mock import Mock

import pytest
from uuid import uuid4
from backend.platform.auth.application.auth_service_impl import AuthenticationServiceImpl
from backend.platform.auth.dto.register_user_request import RegisterUserRequest
from backend.platform.shared.exceptions import UserAlreadyExistsError
from backend.platform.shared.exceptions import InvalidCredentialsError
from tests.factorries import create_user


def test_register_existing_user():
    """
    Registering an existing user raises an exception.
    """

    repository = Mock()
    password_hasher = Mock()
    jwt_service = Mock()

    repository.get_by_identifier.return_value = create_user()

    service = AuthenticationServiceImpl(
        repository,
        password_hasher,
        jwt_service,
    )

    with pytest.raises(UserAlreadyExistsError):
        service.register(
            RegisterUserRequest(
                username="john",
                email="john@example.com",
                password="super-secret-password",
            )
        )

    
def test_refresh_token_user_not_found():
    """
    Refresh fails if the user no longer exists.
    """

    repository = Mock()

    password_hasher = Mock()

    jwt_service = Mock()

    jwt_service.verify_refresh_token.return_value = str(
        uuid4(),
    )

    repository.get_by_id.return_value = None

    service = AuthenticationServiceImpl(
        repository,
        password_hasher,
        jwt_service,
    )

    with pytest.raises(
        InvalidCredentialsError,
    ):
        service.refresh_token(
            "refresh-token",
        )