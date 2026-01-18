from typing import Optional, List, Dict, Any
from sqlalchemy import text

from app.core.database import engine


# ======================================================
# LISTAR LOGS DE IMPORTAÇÃO (AUDITORIA / SUPORTE)
# ======================================================

def listar_import_logs(
    *,
    contrato_id: str,
    tipo_arquivo: Optional[str] = None,
    status: Optional[str] = None,
    error_code: Optional[str] = None,
    usuario_email: Optional[str] = None,
    data_inicio: Optional[str] = None,
    data_fim: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
) -> Dict[str, Any]:
    """
    Lista logs de importação com filtros avançados.

    Retorna:
    - items: lista de logs
    - total: total de registros encontrados (sem paginação)
    """

    filtros = ["contrato_id = :contrato_id"]
    params = {
        "contrato_id": contrato_id,
        "limit": limit,
        "offset": offset,
    }

    if tipo_arquivo:
        filtros.append("tipo_arquivo = :tipo_arquivo")
        params["tipo_arquivo"] = tipo_arquivo

    if status:
        filtros.append("status = :status")
        params["status"] = status

    if error_code:
        filtros.append("error_code = :error_code")
        params["error_code"] = error_code

    if usuario_email:
        filtros.append("usuario_email ILIKE :usuario_email")
        params["usuario_email"] = f"%{usuario_email}%"

    if data_inicio:
        filtros.append("started_at >= :data_inicio")
        params["data_inicio"] = data_inicio

    if data_fim:
        filtros.append("started_at <= :data_fim")
        params["data_fim"] = data_fim

    where_clause = " AND ".join(filtros)

    sql = text(f"""
        SELECT
            id,
            contrato_id,
            sistema_origem_id,
            tipo_arquivo,
            modo_importacao,
            nome_arquivo,
            status,
            error_code,
            mensagem,
            total_registros,
            registros_processados,
            usuario_id,
            usuario_email,
            started_at,
            finished_at
        FROM control.importacoes_log
        WHERE {where_clause}
        ORDER BY started_at DESC
        LIMIT :limit OFFSET :offset
    """)

    count_sql = text(f"""
        SELECT COUNT(*)
        FROM control.importacoes_log
        WHERE {where_clause}
    """)

    with engine.begin() as conn:
        rows = conn.execute(sql, params).mappings().all()
        total = conn.execute(count_sql, params).scalar() or 0

    return {
        "items": [dict(row) for row in rows],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


# ======================================================
# DETALHE DE UM LOG ESPECÍFICO
# ======================================================

def obter_import_log_por_id(
    *,
    log_id: int,
    contrato_id: str
) -> Optional[Dict[str, Any]]:
    """
    Retorna o detalhe de um log específico.
    """

    sql = text("""
        SELECT
            id,
            contrato_id,
            sistema_origem_id,
            tipo_arquivo,
            modo_importacao,
            nome_arquivo,
            status,
            error_code,
            mensagem,
            total_registros,
            registros_processados,
            usuario_id,
            usuario_email,
            started_at,
            finished_at
        FROM control.importacoes_log
        WHERE id = :log_id
          AND contrato_id = :contrato_id
    """)

    with engine.begin() as conn:
        row = conn.execute(
            sql,
            {
                "log_id": log_id,
                "contrato_id": contrato_id
            }
        ).mappings().first()

    return dict(row) if row else None
