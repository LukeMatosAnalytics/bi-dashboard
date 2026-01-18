from fastapi import APIRouter, Depends, Query

from app.core.permissions import somente_admin_ou_master
from app.services.import_logs_service import (
    listar_import_logs,
    obter_import_log_por_id
)
from app.schemas.import_logs_schema import (
    ImportLogItemSchema,
    ImportLogListResponseSchema,
    ImportLogListMetaSchema
)
from app.core.responses import success_response
from app.core.success_codes import SuccessCode


router = APIRouter(
    prefix="/import-logs",
    tags=["Importações / Logs"]
)


# ======================================================
# LISTAR LOGS DE IMPORTAÇÃO
# ======================================================

@router.get(
    "",
    response_model=ImportLogListResponseSchema,
    summary="Listar logs de importação",
    description="""
Retorna o histórico de importações do sistema.

Filtros disponíveis:
- contrato
- tipo de arquivo
- status
- código de erro
- usuário
- período

Usado para auditoria, suporte N2/N3 e monitoramento operacional.
"""
)
def listar_logs(
    contrato_id: str | None = Query(None),
    tipo_arquivo: str | None = Query(None),
    status: str | None = Query(None),
    error_code: str | None = Query(None),
    usuario_email: str | None = Query(None),
    data_inicio: str | None = Query(None),
    data_fim: str | None = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    usuario=Depends(somente_admin_ou_master),
):
    logs, total = listar_import_logs(
        contrato_id=contrato_id or usuario["contrato_id"],
        tipo_arquivo=tipo_arquivo,
        status=status,
        error_code=error_code,
        usuario_email=usuario_email,
        data_inicio=data_inicio,
        data_fim=data_fim,
        limit=limit,
        offset=offset,
    )

    return success_response(
        code=SuccessCode.LIST_SUCCESS,
        data=logs,
        meta={
            "total": total,
            "limit": limit,
            "offset": offset,
        }
    )


# ======================================================
# DETALHE DE UM LOG DE IMPORTAÇÃO
# ======================================================

@router.get(
    "/{log_id}",
    response_model=ImportLogItemSchema,
    summary="Detalhar log de importação",
    description="Retorna todos os detalhes de uma importação específica."
)
def obter_log(
    log_id: int,
    usuario=Depends(somente_admin_ou_master),
):
    log = obter_import_log_por_id(log_id)

    if not log:
        return success_response(
            code=SuccessCode.EMPTY_RESULT,
            data={}
        )

    return success_response(
        code=SuccessCode.DETAIL_SUCCESS,
        data=log
    )
