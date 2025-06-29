from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application settings.
    """
    PROJECT_NAME: str = "DateTree"
    API_PREFIX: str = "/api/v1"
    
    """CORS settings."""
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    """Database settings."""
    DATABASE_URL: str
    
    """JWT Settings."""
    # WARNING: In production, this should be a strong, randomly generated string
    # You can generate one using: openssl rand -hex 32
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"

settings = Settings()