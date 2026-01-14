"""
Configurações da aplicação
"""
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    # Aplicação
    APP_NAME: str = "BI Dashboard API"
    ENVIRONMENT: str = "development"

    # Banco de Dados
    DATABASE_URL: str

    # Segurança JWT
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # CORS
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    model_config = ConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()
