from sqlalchemy import text
from app.core.database import engine


def registrar_importacao(
    contrato_id: str,
    email_usuario: str,
    nome_arquivo: str,
    tipo_arquivo: str,
    quantidade_registros: int | None,
    status: str,
    mensagem_erro: str | None = None
):
    sql = """
    INSERT INTO control.importacoes (
        contrato_id,
        email_usuario,
        nome_arquivo,
        tipo_arquivo,
        quantidade_registros,
        status,
        mensagem_erro
    )
    VALUES (
        :contrato_id,
        :email_usuario,
        :nome_arquivo,
        :tipo_arquivo,
        :quantidade_registros,
        :status,
        :mensagem_erro
    )
    """

    with engine.begin() as conn:
        conn.execute(
            text(sql),
            {
                "contrato_id": contrato_id,
                "email_usuario": email_usuario,
                "nome_arquivo": nome_arquivo,
                "tipo_arquivo": tipo_arquivo,
                "quantidade_registros": quantidade_registros,
                "status": status,
                "mensagem_erro": mensagem_erro
            }
        )
