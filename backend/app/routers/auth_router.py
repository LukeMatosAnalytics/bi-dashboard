"""
Endpoints de autenticação
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import text

from app.core.database import engine
from app.core.security import verificar_senha, criar_token_acesso
from app.core.auth import get_usuario_atual

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Autentica usuário e retorna token JWT
    """
    email = form_data.username
    senha = form_data.password

    sql = """
    SELECT usuario_id, email, senha_hash, nome, role, contrato_id
    FROM control.usuarios
    WHERE email = :email AND status = 'ATIVO' AND ativo = true
    """

    with engine.connect() as conn:
        usuario = conn.execute(
            text(sql),
            {"email": email}
        ).mappings().first()

    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="Usuário ou senha inválidos"
        )

    if not verificar_senha(senha, usuario["senha_hash"]):
        raise HTTPException(
            status_code=401,
            detail="Usuário ou senha inválidos"
        )

    token = criar_token_acesso({
        "sub": usuario["email"],
        "nome": usuario["nome"],
        "role": usuario["role"],
        "contrato_id": usuario["contrato_id"]
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "email": usuario["email"],
            "nome": usuario["nome"],
            "role": usuario["role"],
            "contrato_id": usuario["contrato_id"]
        }
    }


@router.get("/me")
def get_me(usuario=Depends(get_usuario_atual)):
    """
    Retorna dados do usuário autenticado
    """
    return {
        "usuario_id": usuario["usuario_id"],
        "email": usuario["email"],
        "nome": usuario["nome"],
        "role": usuario["role"],
        "contrato_id": usuario["contrato_id"]
    }
