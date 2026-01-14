"""
Controle de permissões por role
"""
from fastapi import Depends, HTTPException, status
from app.core.auth import get_usuario_atual


def somente_master(usuario=Depends(get_usuario_atual)):
    """
    Permite apenas usuários MASTER
    """
    if usuario["role"] != "MASTER":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a MASTER"
        )
    return usuario


def somente_admin_ou_master(usuario=Depends(get_usuario_atual)):
    """
    Permite ADMIN ou MASTER
    """
    if usuario["role"] not in ("ADMIN", "MASTER"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissão insuficiente. Requer ADMIN ou MASTER."
        )
    return usuario


def qualquer_usuario_autenticado(usuario=Depends(get_usuario_atual)):
    """
    Permite qualquer usuário autenticado (MASTER, ADMIN ou USER)
    """
    return usuario
