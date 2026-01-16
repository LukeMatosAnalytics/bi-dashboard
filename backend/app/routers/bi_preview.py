from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_usuario_atual

router = APIRouter(
    prefix="/bi",
    tags=["BI Preview"]
)

@router.get("/os-lanc/preview")
def preview_os_lanc(
    db: Session = Depends(get_db),
    usuario = Depends(get_usuario_atual)
):
    contrato_id = usuario["contrato_id"]

    # 🔹 OS por Situação
    sql_por_situacao = text("""
        SELECT
            CASE ol.situacao
                WHEN 0 THEN 'ABERTO'
                WHEN 1 THEN 'BAIXADO'
                WHEN 2 THEN 'EM COBRANÇA'
                WHEN 3 THEN 'CANCELADO'
                WHEN 4 THEN 'ESTORNADO'
                WHEN 5 THEN 'FECHADO'
                WHEN 6 THEN 'PENDENTE'
                ELSE 'OUTROS'
            END AS label,
            COUNT(*) AS value
        FROM data_pr.os_lanc ol
        WHERE ol.contrato_id = :contrato_id
        GROUP BY label
        ORDER BY value DESC
    """)

    por_situacao = db.execute(
        sql_por_situacao,
        {"contrato_id": contrato_id}
    ).mappings().all()

    # 🔹 OS por Mês (mantém como está)
    sql_por_mes = text("""
        SELECT
            TO_CHAR(dt_lancou, 'YYYY-MM') AS label,
            COUNT(*) AS value
        FROM data_pr.os_lanc
        WHERE contrato_id = :contrato_id
        GROUP BY label
        ORDER BY label
    """)

    por_mes = db.execute(
        sql_por_mes,
        {"contrato_id": contrato_id}
    ).mappings().all()

    return {
        "por_situacao": por_situacao,
        "por_mes": por_mes
    }
