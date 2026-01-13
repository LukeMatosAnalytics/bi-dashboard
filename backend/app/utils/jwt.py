from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings


def criar_token(dados: dict):
    dados_token = dados.copy()

    expira = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    dados_token.update({"exp": expira})

    return jwt.encode(
        dados_token,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

