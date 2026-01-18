from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import engine
from app.core.exceptions import BusinessException
from app.core.errors import ErrorCode


def obter_selos_pendentes_fnc(
    *,
    contrato_id: str,
    data_inicio: str,
    data_fim: str,
):
    """
    Selos que existem na his_selo_detalhe_pr (baixa realizada),
    mas NÃO existem na os_selo (não enviados ao FNC).

    Regras:
    - data raiz: data_ato (quando existir), fallback para created_at
    - contrato/sistema: ancorados em his_selo (hs)
    """

    try:
        sql = text("""
            SELECT DISTINCT
                hsd.selo_principal,
                hs.tipo_ato,
                hsd.id_codigo_ato,
                dca.descricao AS descricao_codigo_ato,
                COALESCE(hsd.data_ato, hsd.created_at) AS data_ato
            FROM data_pr.his_selo_detalhe_pr hsd
            INNER JOIN data_pr.his_selo hs
                    ON hs.selo = hsd.selo_principal
            LEFT JOIN data_pr.os_selo os
                   ON os.selo = hsd.selo_principal
                  AND os.contrato_id = hs.contrato_id
                  AND os.sistema_origem_id = hs.sistema_origem_id
            LEFT JOIN data_pr.dim_codigo_ato dca
                   ON dca.id_codigo_ato = hsd.id_codigo_ato
                  AND COALESCE(hsd.data_ato, hsd.created_at) >= dca.vigencia_inicio
                  AND (
                       dca.vigencia_fim IS NULL
                       OR COALESCE(hsd.data_ato, hsd.created_at) <= dca.vigencia_fim
                  )
            WHERE hs.contrato_id = :contrato_id
              AND COALESCE(hsd.data_ato, hsd.created_at)
                  BETWEEN :data_inicio AND :data_fim
              AND os.selo IS NULL
            ORDER BY data_ato DESC, hsd.selo_principal
        """)

        with engine.connect() as conn:
            registros = conn.execute(
                sql,
                {
                    "contrato_id": contrato_id,
                    "data_inicio": data_inicio,
                    "data_fim": data_fim,
                }
            ).mappings().all()

        return {
            "total_registros": len(registros),
            "registros": registros,
        }

    except SQLAlchemyError as e:
        raise BusinessException(
            error_code=ErrorCode.DATABASE_ERROR,
            detail=str(e)
        )

    except Exception as e:
        raise BusinessException(
            error_code=ErrorCode.UNEXPECTED_ERROR,
            detail=str(e)
        )
