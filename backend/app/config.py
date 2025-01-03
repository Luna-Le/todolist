from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from pathlib import Path

# Get the path to the backend directory
BACKEND_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(
        env_file=str(BACKEND_DIR / ".env"),  # Use absolute path
        env_file_encoding='utf-8'
    )

settings = Settings()