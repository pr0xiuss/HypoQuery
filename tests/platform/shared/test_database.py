from backend.platform.shared.database import (
    SessionLocal,
    verify_database_connection,
)


def test_database_session_creation():
    """
    A SQLAlchemy session can be created.
    """

    session = SessionLocal()

    assert session is not None

    session.close()


def test_verify_database_connection():
    """
    The platform database is reachable.
    """

    verify_database_connection()