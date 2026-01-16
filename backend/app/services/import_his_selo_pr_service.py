import pandas as pd
from sqlalchemy import text
from fastapi import HTTPException

from app.core.database import engine
from app.core.import_config import (
    TIPOS_IMPORTACAO,
    ModoImportacao
)
from app.core.security import verificar_senha_usuario


# ======================================================
# COLUNAS OBRIGATÓRIAS — HIS_SELO
# ======================================================

COLUNAS_OBRIGATORIAS = {
    "id",
    "auto_inc",
    "ativ_sel",
    "tipo_ato",
    "capa",
    "livro",
    "folha",
    "servico",
    "tipo_his",
    "tipo_selo",
    "selo",
    "qtd",
    "dataenvio",
    "numeropedido"
}


# ======================================================
# SERVICE
# ======================================================

def importar_his_selo_pr(
    *,
    file: str,
    contrato_id: str,
    usuario_email: str,
    sistema_origem_id: int,
    modo_importacao: ModoImportacao,
    senha_confirmacao: str | None = None
):
    # --------------------------------------------------
    # 1. Configuração do tipo de importação
    # --------------------------------------------------
    tipo = "his_selo"
    config = TIPOS_IMPORTACAO[tipo]

    if (
        modo_importacao == ModoImportacao.INCREMENTAL
        and not config["permite_incremental"]
    ):
        raise HTTPException(
            status_code=400,
            detail="Este tipo de importação não permite carga incremental"
        )

    # --------------------------------------------------
    # 2. Confirmação de senha (carga inicial)
    # --------------------------------------------------
    if modo_importacao == ModoImportacao.INITIAL:
        if not senha_confirmacao:
            raise HTTPException(
                400,
                "Confirmação de senha obrigatória para carga inicial"
            )

        if not verificar_senha_usuario(
            email=usuario_email,
            senha_plana=senha_confirmacao
        ):
            raise HTTPException(
                403,
                "Senha inválida"
            )

    # --------------------------------------------------
    # 3. Ler Excel
    # --------------------------------------------------
    df = pd.read_excel(file)
    df.columns = df.columns.str.lower()

    # --------------------------------------------------
    # 4. Validar colunas obrigatórias
    # --------------------------------------------------
    faltantes = COLUNAS_OBRIGATORIAS - set(df.columns)

    if faltantes:
        raise HTTPException(
            status_code=400,
            detail=f"Colunas obrigatórias ausentes: {', '.join(sorted(faltantes))}"
        )

    # --------------------------------------------------
    # 5. Manter somente colunas usadas
    # --------------------------------------------------
    df = df[list(COLUNAS_OBRIGATORIAS)]

    # --------------------------------------------------
    # 6. Normalização
    # --------------------------------------------------
    df = df.astype(object)
    df = df.where(pd.notnull(df), None)

    # --------------------------------------------------
    # 7. Remover registros inválidos
    # --------------------------------------------------
    df = df[df["id"].notnull()]

    if df.empty:
        return {
            "status": "SEM_DADOS",
            "registros_processados": 0
        }

    # --------------------------------------------------
    # 8. Colunas de controle
    # --------------------------------------------------
    df["contrato_id"] = contrato_id
    df["sistema_origem_id"] = sistema_origem_id

    registros = df.to_dict("records")

    # --------------------------------------------------
    # 9. DELETE (somente carga inicial)
    # --------------------------------------------------
    delete_sql = text("""
        DELETE FROM data_pr.his_selo
        WHERE contrato_id = :contrato_id
          AND sistema_origem_id = :sistema_origem_id
    """)

    # --------------------------------------------------
    # 10. INSERT
    # --------------------------------------------------
    insert_sql = text("""
        INSERT INTO data_pr.his_selo (
            id,
            auto_inc,
            ativ_sel,
            tipo_ato,
            capa,
            livro,
            folha,
            servico,
            tipo_his,
            tipo_selo,
            selo,
            qtd,
            dataenvio,
            numeropedido,
            contrato_id,
            sistema_origem_id
        ) VALUES (
            :id,
            :auto_inc,
            :ativ_sel,
            :tipo_ato,
            :capa,
            :livro,
            :folha,
            :servico,
            :tipo_his,
            :tipo_selo,
            :selo,
            :qtd,
            :dataenvio,
            :numeropedido,
            :contrato_id,
            :sistema_origem_id
        )
        ON CONFLICT (contrato_id, sistema_origem_id, id)
        DO NOTHING
    """)

    # --------------------------------------------------
    # 11. EXECUÇÃO
    # --------------------------------------------------
    with engine.begin() as conn:
        if modo_importacao == ModoImportacao.INITIAL:
            conn.execute(
                delete_sql,
                {
                    "contrato_id": contrato_id,
                    "sistema_origem_id": sistema_origem_id
                }
            )

        conn.execute(insert_sql, registros)

    return {
        "status": "SUCESSO",
        "modo_importacao": modo_importacao.value,
        "registros_processados": len(registros),
        "sistema_origem_id": sistema_origem_id
    }
