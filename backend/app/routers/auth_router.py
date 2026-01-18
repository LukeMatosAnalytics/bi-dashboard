from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy import text
from jose import JWTError, jwt

from app.core.database import engine
from app.core.security import (
    verificar_senha,
    criar_token_acesso,
    ALGORITHM
)
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    email = form_data.username
    senha = form_data.password

    sql = """
    SELECT usuario_id, email, senha_hash, role, contrato_id
    FROM control.usuarios
    WHERE email = :email
      AND status = 'ATIVO'
    """

    with engine.connect() as conn:
        usuario = conn.execute(
            text(sql),
            {"email": email}
        ).mappings().first()

    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")

    if not verificar_senha(senha, usuario["senha_hash"]):
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")

    token = criar_token_acesso({
        "sub": usuario["email"],
        "role": usuario["role"],
        "contrato_id": usuario["contrato_id"]
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/me")
def me(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[ALGORITHM]
        )
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

    return {
        "email": payload.get("sub"),
        "role": payload.get("role"),
        "contrato_id": payload.get("contrato_id")
    }
