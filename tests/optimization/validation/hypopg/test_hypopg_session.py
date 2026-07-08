from unittest.mock import Mock

from backend.optimization.validation.hypopg.hypopg_session import (
    HypoPGSession,
)


def test_session_create():

    client = Mock()

    session = HypoPGSession(
        client,
    )

    session.create(
        "CREATE INDEX idx_test ON users(id)",
    )

    client.create_index.assert_called_once()


def test_session_cleanup():

    client = Mock()

    session = HypoPGSession(
        client,
    )

    session.cleanup()

    client.reset.assert_called_once()


def test_session_reports_availability():

    client = Mock()

    client.extension_available.return_value = True

    session = HypoPGSession(
        client,
    )

    assert session.available() is True