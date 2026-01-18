from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from app.core.config import settings
from app.core.database import engine
from sqlalchemy import text

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_usuario_logado(token: str = Depends(oauth2_scheme)):
    """
    Retorna o usuário autenticado a partir do JWT
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"]
        )

        email = payload.get("sub")
        contrato_id = payload.get("contrato_id")

        if not email or not contrato_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado"
        )

    # Buscar usuário no banco
    sql = text("""
        SELECT
            id,
            email,
            role,
            contrato_id,
            sistema_origem_id
        FROM control.usuarios
        WHERE email = :email
          AND status = 'ATIVO'
        LIMIT 1
    """)

    with engine.connect() as conn:
        usuario = conn.execute(
            sql,
            {"email": email}
        ).mappings().first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado"
        )

    return usuario
