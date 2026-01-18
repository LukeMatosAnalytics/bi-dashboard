from fastapi import APIRouter

from app.core.errors import ERROR_CATALOG
from app.core.success_catalog import SUCCESS_CATALOG
from app.core.import_config import TIPOS_IMPORTACAO


router = APIRouter(
    prefix="/system",
    tags=["Sistema / Documentação"]
)

# ======================================================
# CATÁLOGO DE ERROS
# ======================================================

@router.get("/error-catalog")
def listar_error_catalog():
    """
    Retorna todos os códigos de erro documentados no sistema.

    Uso:
    - Suporte N2 / N3
    - Auditoria
    - Base de conhecimento
    """

    return {
        "success": True,
        "data": {
            code.value: {
                "message": info["message"],
                "http_status": info["http_status"],
                "action": info.get("action"),
            }
            for code, info in ERROR_CATALOG.items()
        }
    }


# ======================================================
# CATÁLOGO DE SUCESSOS
# ======================================================

@router.get("/success-catalog")
def listar_success_catalog():
    """
    Retorna todos os códigos de sucesso documentados no sistema.
    """

    return {
        "success": True,
        "data": {
            code.value: {
                "message": info["message"]
            }
            for code, info in SUCCESS_CATALOG.items()
        }
    }


# ======================================================
# TIPOS DE IMPORTAÇÃO SUPORTADOS
# ======================================================

@router.get("/import-types")
def listar_tipos_importacao():
    """
    Retorna os tipos de arquivos aceitos para importação
    e suas regras de carga.
    """

    return {
        "success": True,
        "data": {
            tipo: {
                "descricao": config["descricao"],
                "permite_incremental": config["permite_incremental"]
            }
            for tipo, config in TIPOS_IMPORTACAO.items()
        }
    }
