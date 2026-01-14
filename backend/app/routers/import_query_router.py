"""
Endpoints de consulta de importações
"""
from fastapi import APIRouter, Depends
from sqlalchemy import text

from app.core.database import engine
from app.core.permissions import somente_admin_ou_master

router = APIRouter(prefix="/importacoes", tags=["Importações"])


@router.get("/")
def listar_importacoes(usuario=Depends(somente_admin_ou_master)):
    """
    Lista histórico de importações.
    MASTER vê todas, ADMIN vê apenas do seu contrato.
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
        LIMIT 100
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
        LIMIT 100
        """
        params = {"contrato_id": usuario["contrato_id"]}

    with engine.connect() as conn:
        resultado = conn.execute(text(sql), params).mappings().all()

    return [dict(r) for r in resultado]
