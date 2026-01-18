from sqlalchemy import text
from app.core.database import engine


# ======================================================
# CRIA LOG INICIAL
# ======================================================

def criar_log_importacao(
    *,
    contrato_id: str,
    sistema_origem_id: int | None,
    usuario_id: int,
    usuario_email: str,
    tipo_arquivo: str,
    nome_arquivo: str,
    modo_importacao: str,
    total_registros: int,
) -> int:
    """
    Cria o log inicial da importação e retorna o ID.
    """

    sql = text("""
        INSERT INTO control.importacoes_log (
            contrato_id,
            sistema_origem_id,
            usuario_id,
            usuario_email,
            tipo_arquivo,
            modo_importacao,
            nome_arquivo,
            total_registros,
            registros_processados,
            status,
            started_at
        ) VALUES (
            :contrato_id,
            :sistema_origem_id,
            :usuario_id,
            :usuario_email,
            :tipo_arquivo,
            :modo_importacao,
            :nome_arquivo,
            :total_registros,
            0,
            'PROCESSANDO',
            NOW()
        )
        RETURNING id
    """)

    with engine.begin() as conn:
        return conn.execute(
            sql,
            {
                "contrato_id": contrato_id,
                "sistema_origem_id": sistema_origem_id,
                "usuario_id": usuario_id,
                "usuario_email": usuario_email,
                "tipo_arquivo": tipo_arquivo,
                "modo_importacao": modo_importacao,
                "nome_arquivo": nome_arquivo,
                "total_registros": total_registros,
            }
        ).scalar()


# ======================================================
# FINALIZA LOG
# ======================================================

def finalizar_log_importacao(
    *,
    log_id: int,
    status: str,
    registros_processados: int,
    success_code: str | None = None,
    error_code: str | None = None,
    mensagem: str | None = None,
):
    """
    Finaliza o log de importação com sucesso ou erro.
    """

    sql = text("""
        UPDATE control.importacoes_log
        SET
            status = :status,
            registros_processados = :registros_processados,
            success_code = :success_code,
            error_code = :error_code,
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
                "success_code": success_code,
                "error_code": error_code,
                "mensagem": mensagem,
            }
        )


# ======================================================
# FUNÇÃO PADRÃO (USADA PELOS SERVICES)
# ======================================================

def registrar_import_log(
    *,
    usuario_id: int,
    usuario_email: str,
    contrato_id: str,
    sistema_origem_id: int | None,
    tipo_arquivo: str,
    modo_importacao: str,
    nome_arquivo: str,
    total_registros: int,
    registros_processados: int,
    status: str,
    success_code: str | None = None,
    error_code: str | None = None,
    mensagem: str | None = None,
):
    """
    Cria e finaliza o log de importação.
    """

    log_id = criar_log_importacao(
        usuario_id=usuario_id,
        usuario_email=usuario_email,
        contrato_id=contrato_id,
        sistema_origem_id=sistema_origem_id,
        tipo_arquivo=tipo_arquivo,
        modo_importacao=modo_importacao,
        nome_arquivo=nome_arquivo,
        total_registros=total_registros,
    )

    finalizar_log_importacao(
        log_id=log_id,
        status=status,
        registros_processados=registros_processados,
        success_code=success_code,
        error_code=error_code,
        mensagem=mensagem,
    )
