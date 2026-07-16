from collections.abc import Generator
from pathlib import Path
import sys
from psycopg import OperationalError
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
from backend.shared.db import get_connection
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.orm import Session

from backend.api.main import app
from backend.platform.shared.database import (
    SessionLocal,
)


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    """
    Returns a SQLAlchemy database session.

    Rolls back all changes after each test.
    """

    session = SessionLocal()

    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture(scope="session")
def client() -> Generator[TestClient, None, None]:
    """
    Shared FastAPI test client.
    """

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def verify_database(db_session: Session) -> None:
    """
    Ensures the platform database is reachable.
    """

    db_session.execute(
        text("SELECT 1"),
    )


@pytest.fixture
def db_connection():
    """
    Returns a PostgreSQL connection.

    Skips the test if PostgreSQL is unavailable.
    """

    try:
        connection = get_connection()
    except OperationalError:
        pytest.skip("PostgreSQL is not running.")

    yield connection

    connection.close()