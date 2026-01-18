from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import engine
from app.core.exceptions import BusinessException
from app.core.error_codes import ErrorCode


def obter_selos_duplicados_mesmo_sistema(
    *,
    contrato_id: str,
    data_inicio: str,
    data_fim: str
):
    """
    Selos duplicados no MESMO sistema_origem_id
    (erro operacional interno).
    """

    try:
        with engine.connect() as conn:
            sql = text("""
                SELECT
                    hsd.selo_principal,
                    hsd.sistema_origem_id,
                    hs.tipo_ato,
                    hs.livro,
                    hs.folha,
                    hsd.dataato,
                    COUNT(*) AS total_ocorrencias
                FROM data_pr.his_selo_detalhe_pr hsd
                LEFT JOIN data_pr.his_selo hs
                       ON hs.selo = hsd.selo_principal
                      AND hs.contrato_id = hsd.contrato_id
                      AND hs.sistema_origem_id = hsd.sistema_origem_id
                WHERE hsd.dataato BETWEEN :data_inicio AND :data_fim
                  AND hsd.contrato_id = :contrato_id
                GROUP BY
                    hsd.selo_principal,
                    hsd.sistema_origem_id,
                    hs.tipo_ato,
                    hs.livro,
                    hs.folha,
                    hsd.dataato
                HAVING COUNT(*) > 1
                ORDER BY total_ocorrencias DESC, hsd.selo_principal
            """)

            registros = conn.execute(
                sql,
                {
                    "data_inicio": data_inicio,
                    "data_fim": data_fim,
                    "contrato_id": contrato_id,
                }
            ).mappings().all()

            return {
                "tipo_duplicidade": "MESMO_SISTEMA",
                "total_selos": len(registros),
                "registros": registros
            }

    except SQLAlchemyError as e:
        raise BusinessException(
            error_code=ErrorCode.DB_001,
            message="Erro ao consultar selos duplicados no mesmo sistema",
            detail=str(e),
            action="Verificar dados da his_selo_detalhe_pr"
        )


def obter_selos_duplicados_sistemas_diferentes(
    *,
    contrato_id: str,
    data_inicio: str,
    data_fim: str
):
    """
    Selos duplicados em SISTEMAS_ORIGEM diferentes
    (erro grave de integração).
    """

    try:
        with engine.connect() as conn:
            sql = text("""
                SELECT
                    hsd.selo_principal,
                    COUNT(DISTINCT hsd.sistema_origem_id) AS total_sistemas,
                    ARRAY_AGG(DISTINCT hsd.sistema_origem_id) AS sistemas_origem,
                    MIN(hsd.dataato) AS primeira_ocorrencia,
                    MAX(hsd.dataato) AS ultima_ocorrencia
                FROM data_pr.his_selo_detalhe_pr hsd
                WHERE hsd.dataato BETWEEN :data_inicio AND :data_fim
                  AND hsd.contrato_id = :contrato_id
                GROUP BY hsd.selo_principal
                HAVING COUNT(DISTINCT hsd.sistema_origem_id) > 1
                ORDER BY total_sistemas DESC, hsd.selo_principal
            """)

            registros = conn.execute(
                sql,
                {
                    "data_inicio": data_inicio,
                    "data_fim": data_fim,
                    "contrato_id": contrato_id,
                }
            ).mappings().all()

            return {
                "tipo_duplicidade": "SISTEMAS_DIFERENTES",
                "total_selos": len(registros),
                "registros": registros
            }

    except SQLAlchemyError as e:
        raise BusinessException(
            error_code=ErrorCode.DB_001,
            message="Erro ao consultar selos duplicados em sistemas diferentes",
            detail=str(e),
            action="Verificar integração entre sistemas"
        )
