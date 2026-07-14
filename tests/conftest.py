from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from collections.abc import Generator
from fastapi.testclient import TestClient

from backend.api.main import app

import pytest
from psycopg import OperationalError

from backend.shared.db import get_connection

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


@pytest.fixture(scope="session")
def client() -> Generator[TestClient, None, None]:
    """
    Shared FastAPI test client.
    """

    with TestClient(app) as test_client:
        yield test_client