from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import text

from app.core.database import engine
from app.core.security import verificar_senha, criar_token_acesso

router = APIRouter(prefix="/auth", tags=["Auth"])


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
        raise HTTPException(401, "Usuário ou senha inválidos")

    if not verificar_senha(senha, usuario["senha_hash"]):
        raise HTTPException(401, "Usuário ou senha inválidos")

    token = criar_token_acesso({
        "sub": usuario["email"],
        "role": usuario["role"],
        "contrato_id": usuario["contrato_id"]
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }
