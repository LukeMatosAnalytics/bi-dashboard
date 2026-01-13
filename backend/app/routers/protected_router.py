from fastapi import APIRouter, Depends
from app.core.permissions import somente_admin_ou_master

router = APIRouter(prefix="/protected", tags=["Protected"])


@router.get("/teste")
def rota_protegida(usuario=Depends(somente_admin_ou_master)):
    return {
        "mensagem": "Acesso autorizado",
        "usuario": usuario
    }
