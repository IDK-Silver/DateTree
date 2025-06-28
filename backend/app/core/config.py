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

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"

settings = Settings()