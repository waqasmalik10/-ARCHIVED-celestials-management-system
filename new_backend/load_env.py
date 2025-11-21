import os
import logging
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# --- Define environment schema ---
class EnvSchema(BaseSettings):
    # Database connection URL
    data_base_url: str \

    # JWT configuration
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # Pydantic settings configuration
    model_config = SettingsConfigDict(
        env_file=".env",            # Load from .env file
        case_sensitive=False,       # Case insensitive keys
        populate_by_name=True       # Populate fields by environment variable names
    )


# --- Load environment safely ---
def load_environment() -> EnvSchema:
    try:
        # Try loading environment variables
        env = EnvSchema()
        return env
    except Exception as e:
        # Fallback in case of validation error
        logging.warning(f"Environment validation failed! Using default values. {e}")
        return EnvSchema()


# --- Helper getter functions ---
def get_database_url() -> str:
    # Return database URL from environment
    env = load_environment()
    return env.data_base_url


def get_secret_key() -> str:
    # Return JWT secret key from environment
    env = load_environment()
    return env.secret_key


def get_algorithm() -> str:
    # Return JWT algorithm from environment
    env = load_environment()
    return env.algorithm


def get_token_expire_minutes() -> int:
    # Return access token expiration minutes
    env = load_environment()
    return env.access_token_expire_minutes


# --- Quick test (optional) ---
if __name__ == "__main__":
    # Print environment values for verification
    print(get_database_url())
    print(get_secret_key())
    print(get_algorithm())
    print(get_token_expire_minutes())
