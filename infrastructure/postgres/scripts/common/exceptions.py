class SeederError(Exception):
    """Base exception for all seeder errors."""


class DatabaseConnectionError(SeederError):
    """Raised when a database connection cannot be established."""


class DataGenerationError(SeederError):
    """Raised when data generation fails."""


class ValidationError(SeederError):
    """Raised when seeded data validation fails."""