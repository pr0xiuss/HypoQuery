from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Global application settings.

    Values are loaded from environment variables and the .env file.
    """

    app_name: str = Field(
        default="HypoQuery",
        description="Application name.",
    )

    app_version: str = Field(
        default="1.0.0",
        description="Application version.",
    )

    environment: str = Field(
        default="development",
        description="Current application environment.",
    )

    debug: bool = Field(
        default=True,
        description="Enable debug mode.",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    database_host: str = Field(
        default="localhost",
        validation_alias="POSTGRES_HOST",
    )

    database_port: int = Field(
        default=5432,
        validation_alias="POSTGRES_PORT",
    )

    database_name: str = Field(
        default="hypoquery_platform",
        validation_alias="PLATFORM_POSTGRES_DB",
    )

    target_database_name: str = Field(
        default="hypoquery",
        validation_alias="POSTGRES_DB",
    )

    database_user: str = Field(
        default="postgres",
        validation_alias="POSTGRES_USER",
    )

    database_password: str = Field(
        default="postgres",
        validation_alias="POSTGRES_PASSWORD",
    )

    jwt_secret: str = Field(
        default="change-me-in-production",
        description="JWT signing secret.",
    )

    jwt_algorithm: str = Field(
        default="HS256",
    )

    jwt_expiration_minutes: int = Field(
        default=60,
    )

@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached Settings instance.

    The settings object is created only once during the
    application's lifetime.
    """
    return Settings()