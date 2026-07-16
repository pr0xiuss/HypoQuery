from backend.platform.config.settings import get_settings


def test_settings_load():
    """
    Settings are loaded successfully.
    """

    settings = get_settings()

    assert settings.app_name == "HypoQuery"


def test_database_settings():
    """
    Database settings are available.
    """

    settings = get_settings()

    assert settings.database_host
    assert settings.database_port > 0
    assert settings.database_name
    assert settings.database_user


def test_jwt_settings():
    """
    JWT settings are available.
    """

    settings = get_settings()

    assert settings.jwt_secret
    assert settings.jwt_algorithm == "HS256"
    assert settings.jwt_expiration_minutes > 0