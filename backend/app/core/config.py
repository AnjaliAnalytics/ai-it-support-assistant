from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI-Powered IT Support & Incident Resolution Assistant"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    PORT: int = 8000
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    GEMINI_API_KEY: str = ""
    BACKEND_CORS_ORIGINS: List[Union[AnyHttpUrl, str]] = [
        "http://localhost:8501",
        "http://127.0.0.1:8501",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()