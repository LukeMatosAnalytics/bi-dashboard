from sqlalchemy import text
from app.core.database import engine


def listar_importacoes(usuario: dict):
    """
    Retorna o histórico de importações.
    MASTER vê tudo.
    ADMIN vê apenas do próprio contrato.
    """

    if usuario["role"] == "MASTER":
        sql = """
        SELECT
            importacao_id,
            contrato_id,
            email_usuario,
            nome_arquivo,
            tipo_arquivo,
            quantidade_registros,
            status,
            mensagem_erro,
            criado_em
        FROM control.importacoes
        ORDER BY criado_em DESC
        """
        params = {}
    else:
        sql = """
        SELECT
            importacao_id,
            contrato_id,
            email_usuario,
            nome_arquivo,
            tipo_arquivo,
            quantidade_registros,
            status,
            mensagem_erro,
            criado_em
        FROM control.importacoes
        WHERE contrato_id = :contrato_id
        ORDER BY criado_em DESC
        """
        params = {"contrato_id": usuario["contrato_id"]}

    with engine.connect() as conn:
        resultado = conn.execute(
            text(sql),
            params
        ).mappings().all()

    return resultado
