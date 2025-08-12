from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Personal Website API"
    
    # CORS Settings
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # Database Settings
    DATABASE_URL: Optional[str] = None
    
    # Email Settings
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[str] = None
    EMAILS_FROM_NAME: Optional[str] = None
    
    # Security Settings
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # AI Search Settings
    OPENAI_API_KEY: Optional[str] = None
    SEARCH_INDEX_PATH: str = "data/search_index"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
