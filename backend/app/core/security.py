from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import text

from app.core.config import settings
from app.core.database import engine

# ==============================
# CONFIGURAÇÕES DE SENHA
# ==============================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def gerar_hash_senha(senha: str) -> str:
    """
    Gera hash bcrypt para armazenamento no banco.
    O bcrypt só considera os primeiros 72 bytes.
    """
    senha = senha[:72]
    return pwd_context.hash(senha)


def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    """
    Compara senha digitada com hash salvo.

    Boa prática:
    - Limita a senha a 72 bytes (limite do bcrypt)
    - Evita erro e comportamento inseguro
    """
    senha_plana = senha_plana[:72]
    return pwd_context.verify(senha_plana, senha_hash)


def verificar_senha_usuario(*, email: str, senha_plana: str) -> bool:
    """
    Valida a senha do usuário consultando o banco
    """
    sql = text("""
        SELECT senha_hash
        FROM control.usuarios
        WHERE email = :email
          AND ativo = TRUE
        LIMIT 1
    """)

    with engine.begin() as conn:
        result = conn.execute(sql, {"email": email}).fetchone()

    if not result:
        return False

    senha_hash = result[0]
    return verificar_senha(senha_plana, senha_hash)


# ==============================
# CONFIGURAÇÕES JWT
# ==============================

ALGORITHM = "HS256"


def criar_token_acesso(
    dados: dict,
    expires_delta: Optional[timedelta] = None
):
    """
    Cria token JWT de acesso
    """
    to_encode = dados.copy()

    expire = datetime.utcnow() + (
        expires_delta
        if expires_delta
        else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt
