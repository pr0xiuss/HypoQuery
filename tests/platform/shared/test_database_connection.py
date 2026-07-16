from sqlalchemy import text


def test_database_connection(
    db_session,
):
    """
    The platform database is reachable.
    """

    result = db_session.execute(
        text("SELECT 1"),
    )

    assert result.scalar() == 1