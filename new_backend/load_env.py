import logging
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import ValidationError


# --- Define environment schema ---
class EnvSchema(BaseSettings):
    # Database connection
    data_base_url: str

    # JWT Config
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        populate_by_name=True
    )


# --- Strict Loader (fails fast) ---
def load_environment() -> EnvSchema:
    try:
        return EnvSchema()
    except ValidationError as e:
        logging.critical("❌ Missing or invalid environment variables!")
        logging.critical(e)
        raise SystemExit(
            "\n🚫 Application stopped. Fix your .env file before running again.\n"
        )


# --- Helper getters ---
def get_database_url() -> str:
    return load_environment().data_base_url


def get_secret_key() -> str:
    return load_environment().secret_key


def get_algorithm() -> str:
    return load_environment().algorithm


def get_token_expire_minutes() -> int:
    return load_environment().access_token_expire_minutes


# --- Quick manual test ---
if __name__ == "__main__":
    load_environment()
    print("✅ Environment OK")
    print(get_database_url())
    print(get_secret_key())
    print(get_algorithm())
    print(get_token_expire_minutes())
