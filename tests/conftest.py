from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(PROJECT_ROOT))

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