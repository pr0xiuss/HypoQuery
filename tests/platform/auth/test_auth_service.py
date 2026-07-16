from unittest.mock import Mock

from backend.platform.auth.application.auth_service_impl import (
    AuthenticationServiceImpl,
)
from backend.platform.auth.dto.register_user_request import (
    RegisterUserRequest,
)
from backend.platform.auth.dto.login_request import (
    LoginRequest,
)
from tests.factorries import create_user


def test_register_user():
    """
    Users can register successfully.
    """

    repository = Mock()
    password_hasher = Mock()
    jwt_service = Mock()

    password_hasher.hash.return_value = "hashed-password"

    repository.get_by_identifier.return_value = None
    repository.save.return_value = create_user()

    service = AuthenticationServiceImpl(
        repository,
        password_hasher,
        jwt_service,
    )

    request = RegisterUserRequest(
        username="john",
        email="john@example.com",
        password="super-secret-password",
    )

    response = service.register(
        request,
    )

    assert response.username == "john"


def test_login():
    """
    Users can authenticate successfully.
    """

    repository = Mock()
    password_hasher = Mock()
    jwt_service = Mock()

    user = create_user()

    repository.get_by_identifier.return_value = user
    password_hasher.verify.return_value = True
    jwt_service.create_access_token.return_value = "jwt-token"

    service = AuthenticationServiceImpl(
        repository,
        password_hasher,
        jwt_service,
    )

    response = service.login(
        LoginRequest(
            identifier="john",
            password="super-secret-password",
        )
    )

    assert response.access_token == "jwt-token"