import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI-Powered IT Support & Incident Resolution Assistant"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    GEMINI_API_KEY: str = ""
    DATABASE_URL: str = "sqlite:///./test_sqlite.db"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()