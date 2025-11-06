import os
import logging
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# --- Define environment schema ---
class EnvSchema(BaseSettings):
    # Database connection
    data_base_url: str \

    # JWT Config
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        populate_by_name=True
    )


# --- Load environment safely ---
def load_environment() -> EnvSchema:
    try:
        env = EnvSchema()
        return env
    except Exception as e:
        logging.warning(f"Environment validation failed! Using default values. {e}")
        return EnvSchema()


# --- Helper getters ---
def get_database_url() -> str:
    env = load_environment()
    return env.data_base_url


def get_secret_key() -> str:
    env = load_environment()
    return env.secret_key


def get_algorithm() -> str:
    env = load_environment()
    return env.algorithm


def get_token_expire_minutes() -> int:
    env = load_environment()
    return env.access_token_expire_minutes


# --- Quick test (optional) ---
if __name__ == "__main__":
    print(get_database_url())
    print(get_secret_key())
    print(get_algorithm())
    print(get_token_expire_minutes())