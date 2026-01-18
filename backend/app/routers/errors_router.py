from fastapi import APIRouter

from app.core.errors import ERROR_CATALOG

router = APIRouter(
    prefix="/errors",
    tags=["Documentação de Erros"]
)


@router.get("/catalog")
def listar_catalogo_erros():
    """
    Catálogo oficial de erros da aplicação.
    Usado para suporte técnico (N2/N3) e auditoria.
    """

    return {
        "success": True,
        "data": [
            {
                "error_code": code,
                "http_status": info["http_status"],
                "message": info["message"],
                "action": info.get("action"),
            }
            for code, info in ERROR_CATALOG.items()
        ]
    }
