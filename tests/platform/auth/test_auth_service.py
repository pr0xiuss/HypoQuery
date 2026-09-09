from unittest.mock import Mock

from backend.platform.auth.application.auth_service_impl import (
    AuthenticationServiceImpl,
)
from backend.platform.auth.dto.login_request import (
    LoginRequest,
)
from backend.platform.auth.dto.register_user_request import (
    RegisterUserRequest,
)
from tests.factories import create_user


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

    response = service.register(
        RegisterUserRequest(
            username="john",
            email="john@example.com",
            password="super-secret-password",
        ),
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

    jwt_service.create_access_token.return_value = "access-token"
    jwt_service.create_refresh_token.return_value = "refresh-token"
    jwt_service.access_token_expires_in.return_value = 1800

    service = AuthenticationServiceImpl(
        repository,
        password_hasher,
        jwt_service,
    )

    response = service.login(
        LoginRequest(
            identifier="john",
            password="super-secret-password",
        ),
    )

    assert response.access_token == "access-token"
    assert response.refresh_token == "refresh-token"
    assert response.expires_in == 1800
    assert response.token_type == "Bearer"


def test_refresh_token():
    """
    Access tokens can be refreshed.
    """

    repository = Mock()
    password_hasher = Mock()
    jwt_service = Mock()

    user = create_user()

    repository.get_by_id.return_value = user

    jwt_service.verify_refresh_token.return_value = str(
        user.id,
    )

    jwt_service.create_access_token.return_value = (
        "new-access-token"
    )

    jwt_service.access_token_expires_in.return_value = (
        1800
    )

    service = AuthenticationServiceImpl(
        repository,
        password_hasher,
        jwt_service,
    )

    response = service.refresh_token(
        "refresh-token",
    )

    assert response.access_token == "new-access-token"