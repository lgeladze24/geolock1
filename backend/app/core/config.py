from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

class Settings(BaseSettings):
    # Project info
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "GeoLock")
    VERSION: str = os.getenv("VERSION", "1.0.0")
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Validate that required environment variables are set
def validate_settings(settings: Settings) -> None:
    missing_vars = []
    if not settings.DATABASE_URL:
        missing_vars.append("DATABASE_URL")
    if not settings.SECRET_KEY:
        missing_vars.append("SECRET_KEY")

    if missing_vars:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )


# Create settings instance
settings = Settings()

# Validate settings
validate_settings(settings)