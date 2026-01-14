"""
Autenticação e autorização
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy import text

from app.core.database import engine
from app.core.security import decodificar_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_usuario_atual(token: str = Depends(oauth2_scheme)):
    """
    Dependência que retorna o usuário autenticado
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = decodificar_token(token)
        email: str = payload.get("sub")
        
        if email is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    # Busca usuário no banco
    sql = """
    SELECT usuario_id, email, nome, role, contrato_id, ativo
    FROM control.usuarios
    WHERE email = :email AND ativo = true
    """
    
    with engine.connect() as conn:
        usuario = conn.execute(
            text(sql),
            {"email": email}
        ).mappings().first()
    
    if not usuario:
        raise credentials_exception
    
    return dict(usuario)
