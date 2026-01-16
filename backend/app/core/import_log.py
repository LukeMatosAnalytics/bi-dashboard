from sqlalchemy import text
from app.core.database import engine


def criar_log_importacao(
    *,
    contrato_id: str,
    sistema_origem_id: int,
    usuario_email: str,
    tipo_arquivo: str,
    modo_importacao: str,
    nome_arquivo: str | None = None,
    total_registros: int | None = None
) -> int:
    """
    Cria o log inicial da importação.
    Retorna o ID do log para atualizações futuras.
    """

    sql = text("""
        INSERT INTO control.importacoes_log (
            contrato_id,
            sistema_origem_id,
            usuario_email,
            tipo_arquivo,
            modo_importacao,
            nome_arquivo,
            total_registros,
            status
        ) VALUES (
            :contrato_id,
            :sistema_origem_id,
            :usuario_email,
            :tipo_arquivo,
            :modo_importacao,
            :nome_arquivo,
            :total_registros,
            'PROCESSANDO'
        )
        RETURNING id
    """)

    with engine.begin() as conn:
        log_id = conn.execute(
            sql,
            {
                "contrato_id": contrato_id,
                "sistema_origem_id": sistema_origem_id,
                "usuario_email": usuario_email,
                "tipo_arquivo": tipo_arquivo,
                "modo_importacao": modo_importacao,
                "nome_arquivo": nome_arquivo,
                "total_registros": total_registros
            }
        ).scalar()

    return log_id


def atualizar_log_importacao(
    *,
    log_id: int,
    status: str,
    registros_processados: int | None = None,
    mensagem: str | None = None
):
    """
    Atualiza o log de importação ao final do processo.
    """

    sql = text("""
        UPDATE control.importacoes_log
        SET
            status = :status,
            registros_processados = :registros_processados,
            mensagem = :mensagem,
            finished_at = NOW()
        WHERE id = :log_id
    """)

    with engine.begin() as conn:
        conn.execute(
            sql,
            {
                "log_id": log_id,
                "status": status,
                "registros_processados": registros_processados,
                "mensagem": mensagem
            }
        )
