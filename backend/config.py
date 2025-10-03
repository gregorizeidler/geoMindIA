"""
Configuration management for GeoMindIA
"""
import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # API Keys
    gemini_api_key: str = ""
    google_maps_api_key: str = ""
    
    # Database
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "geospatial_ai"
    db_user: str = "postgres"
    db_password: str = "postgres"
    
    # Server
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # Application
    app_name: str = "GeoMindIA"
    debug: bool = False
    
    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()

