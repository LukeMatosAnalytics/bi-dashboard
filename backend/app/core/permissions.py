from fastapi import Depends, HTTPException, status
from app.core.auth import get_usuario_atual


def somente_admin_ou_master(usuario=Depends(get_usuario_atual)):
    if usuario["role"] not in ("ADMIN", "MASTER"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissão insuficiente"
        )
    return usuario
