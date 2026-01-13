from fastapi import APIRouter, Depends

from app.core.permissions import somente_admin_ou_master
from app.services.import_query_service import listar_importacoes

router = APIRouter(
    prefix="/importacoes",
    tags=["Importações"]
)


@router.get("/")
def consultar_importacoes(usuario=Depends(somente_admin_ou_master)):
    return listar_importacoes(usuario)
