from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, PostgresDsn, field_validator
from typing import Optional

class Settings(BaseSettings):
    """
    Manages application-wide settings, loading from environment variables.
    Utilizes Pydantic's BaseSettings for robust validation and type-checking.
    """
    # --- Application Core Settings ---
    # Why: Defines basic application metadata.
    APP_NAME: str = "Agentic TaskOps API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False, description="Enable debug mode (DO NOT use in production).")

    # --- Database Settings ---
    # Why: Connection string for the primary database. Must be a valid PostgreSQL DSN.
    # It's a required field; the app will not start without it.
    DATABASE_URL: PostgresDsn = Field(..., description="PostgreSQL connection URL for the application (async).")
    ALEMBIC_DATABASE_URL: Optional[PostgresDsn] = Field(None, description="PostgreSQL connection URL for Alembic (sync).")

    # --- Security & JWT Settings ---
    # Why: Manages the secret key for signing JWTs and token lifetime.
    # The secret key is critical for security and must be kept private.
    SECRET_KEY: str = Field(..., description="Secret key for signing JWT tokens.")
    ALGORITHM: str = Field(default="HS256", description="Algorithm used for JWT signing.")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, description="Lifetime of access tokens in minutes.")

    @field_validator("SECRET_KEY", "ALGORITHM")
    @classmethod
    def strip_quotes(cls, v: str) -> str:
        """
        Strips leading/trailing single and double quotes from a string.
        """
        return v.strip("'\"")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        case_sensitive=False, # Allows uppercase environment variables to map to lowercase fields
    )

# Instantiate the settings object that will be used across the application.
settings = Settings()
