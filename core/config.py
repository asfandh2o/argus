from pydantic_settings import BaseSettings
from typing import List
import json


class Settings(BaseSettings):
    # App
    APP_NAME: str = "ARGUS"
    ENVIRONMENT: str = "development"
    SECRET_KEY: str = "argus-dev-secret-change-in-production"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://argus:argus_password@db:5432/argus_db"

    # Redis
    REDIS_URL: str = "redis://redis:6379/0"

    # CORS
    CORS_ORIGINS: str = '["http://localhost:3002"]'

    # LLM
    LLM_PROVIDER: str = "groq"
    GROQ_API_KEY: str = ""
    LLM_MODEL: str = "llama-3.3-70b-versatile"

    # Admin credentials
    ADMIN_EMAIL: str = "admin@nora.ai"
    ADMIN_PASSWORD: str = "admin123"

    # HERA integration
    HERA_API_URL: str = "http://host.docker.internal:8001"
    HERA_API_KEY: str = ""

    # ECHO integration
    ECHO_API_URL: str = "http://host.docker.internal:8000"
    ECHO_API_KEY: str = ""

    # Data collection
    COLLECTION_INTERVAL_MINUTES: int = 30

    @property
    def cors_origins_list(self) -> List[str]:
        try:
            return json.loads(self.CORS_ORIGINS)
        except (json.JSONDecodeError, TypeError):
            return ["http://localhost:3002"]

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
