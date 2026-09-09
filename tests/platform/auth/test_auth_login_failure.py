from unittest.mock import Mock

import pytest

from backend.platform.auth.application.auth_service_impl import (
    AuthenticationServiceImpl,
)
from backend.platform.auth.dto.login_request import (
    LoginRequest,
)
from backend.platform.shared.exceptions import (
    InvalidCredentialsError,
)
from tests.factories import create_user


def test_login_invalid_password():
    """
    Invalid passwords cannot authenticate.
    """

    repository = Mock()
    password_hasher = Mock()
    jwt_service = Mock()

    repository.get_by_identifier.return_value = create_user()
    password_hasher.verify.return_value = False

    service = AuthenticationServiceImpl(
        repository,
        password_hasher,
        jwt_service,
    )

    with pytest.raises(
        InvalidCredentialsError,
    ):
        service.login(
            LoginRequest(
                identifier="john",
                password="wrong-password",
            )
        )


def test_login_unknown_user():
    """
    Unknown users cannot authenticate.
    """

    repository = Mock()
    password_hasher = Mock()
    jwt_service = Mock()

    repository.get_by_identifier.return_value = None

    service = AuthenticationServiceImpl(
        repository,
        password_hasher,
        jwt_service,
    )

    with pytest.raises(
        InvalidCredentialsError,
    ):
        service.login(
            LoginRequest(
                identifier="unknown",
                password="password",
            )
        )