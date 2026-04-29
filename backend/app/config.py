"""Configurações da aplicação"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Configurações gerais da aplicação"""
    
    # Aplicação
    app_name: str = "SistemaSimples"
    app_version: str = "1.0.0"
    debug: bool = True
    environment: str = "development"
    
    # Database
    database_url: str = "sqlite:///./test.db"
    db_user: str = "postgres"
    db_password: str = "postgres"
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "sistema_simples"
    
    # Security
    secret_key: str = "sua-chave-secreta-super-segura-mudar-em-producao"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ]
    
    # API
    api_prefix: str = "/api/v1"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
