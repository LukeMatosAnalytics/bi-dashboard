from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    # ==============================
    # APLICAÇÃO
    # ==============================
    APP_NAME: str = "BI Dashboard API"
    ENVIRONMENT: str = "development"

    # ==============================
    # BANCO DE DADOS
    # ==============================
    DATABASE_URL: str

    # ==============================
    # SEGURANÇA / JWT
    # ==============================
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # ==============================
    # CONFIG
    # ==============================
    model_config = ConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()
