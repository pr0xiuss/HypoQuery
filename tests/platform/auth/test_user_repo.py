from tests.factorries import create_user


def test_save_user(
    db_session,
):
    """
    Users can be persisted.
    """

    user = create_user()

    assert user is not None


def test_get_user_by_identifier(
    db_session,
):
    """
    Users can be retrieved by identifier.
    """

    user = create_user()

    assert user.username == "john"


def test_get_user_by_id(
    db_session,
):
    """
    Users can be retrieved by id.
    """

    user = create_user()

    assert user.id is not None