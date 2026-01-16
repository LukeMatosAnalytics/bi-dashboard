import pandas as pd
from sqlalchemy import text
from fastapi import HTTPException

from app.core.database import engine
from app.core.import_config import (
    TIPOS_IMPORTACAO,
    ModoImportacao
)
from app.core.security import verificar_senha_usuario
from app.core.import_log import (
    criar_log_importacao,
    atualizar_log_importacao
)


# ======================================================
# COLUNAS OBRIGATÓRIAS
# ======================================================

COLUNAS_OBRIGATORIAS = {
    "recordnumber",

    "selo_principal",
    "selo_retificacao",
    "selo_anulacao",
    "selo_cancelamento",
    "seloretificado",

    "codtipoato",
    "id_codigo_ato",

    "numpedido",
    "protocolo",
    "documento",

    "chavedigital",
    "qrcode",
    "caminhoimagem",
    "json",

    "valorbase",
    "divisor",
    "quantidade",

    "funrejus",
    "iss",
    "fadep",
    "funarpen",

    "cartorio",
    "distribuidor",

    "planilha_ag_contraente2_nome_adotado",
    "planilha_ag_contraente2_cpf",

    "status",
    "mensagem",

    "id_tipo_gratuidade",
    "id_usuario"
}


# ======================================================
# SERVICE
# ======================================================

def importar_his_selo_detalhe_pr(
    *,
    file: str,
    contrato_id: str,
    usuario_email: str,
    senha_confirmacao: str | None,
    sistema_origem_id: int,
    modo_importacao: ModoImportacao,
    nome_arquivo: str | None = None
):
    tipo_arquivo = "his_selo_detalhe_pr"
    log_id = None

    try:
        # --------------------------------------------------
        # LOG - início
        # --------------------------------------------------
        log_id = criar_log_importacao(
            contrato_id=contrato_id,
            sistema_origem_id=sistema_origem_id,
            usuario_email=usuario_email,
            tipo_arquivo=tipo_arquivo,
            modo_importacao=modo_importacao.value,
            nome_arquivo=nome_arquivo
        )

        # --------------------------------------------------
        # 1. Validar tipo de importação
        # --------------------------------------------------
        config = TIPOS_IMPORTACAO[tipo_arquivo]

        if (
            modo_importacao == ModoImportacao.INCREMENTAL
            and not config["permite_incremental"]
        ):
            raise HTTPException(
                status_code=400,
                detail="Este tipo de importação não permite carga incremental"
            )

        # --------------------------------------------------
        # 2. Validar senha se carga inicial
        # --------------------------------------------------
        if modo_importacao == ModoImportacao.INITIAL:
            if not senha_confirmacao:
                raise HTTPException(
                    status_code=400,
                    detail="Confirmação de senha é obrigatória para carga inicial"
                )

            if not verificar_senha_usuario(
                email=usuario_email,
                senha_plana=senha_confirmacao
            ):
                raise HTTPException(
                    status_code=403,
                    detail="Senha inválida"
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
            raise ValueError(
                f"Colunas obrigatórias ausentes: {', '.join(sorted(faltantes))}"
            )

        # --------------------------------------------------
        # 5. Selecionar colunas usadas
        # --------------------------------------------------
        df = df[list(COLUNAS_OBRIGATORIAS)]

        # --------------------------------------------------
        # 6. Normalização
        # --------------------------------------------------
        df = df.astype(object)
        df = df.where(pd.notnull(df), None)

        df = df.rename(columns={
            "planilha_ag_contraente2_nome_adotado": "contraente_nome",
            "planilha_ag_contraente2_cpf": "contraente_cpf"
        })

        df = df[df["recordnumber"].notnull()]

        # --------------------------------------------------
        # 7. Colunas de controle
        # --------------------------------------------------
        df["contrato_id"] = contrato_id
        df["sistema_origem_id"] = sistema_origem_id

        registros = df.to_dict("records")

        if not registros:
            atualizar_log_importacao(
                log_id=log_id,
                status="SEM_DADOS",
                registros_processados=0
            )
            return {
                "status": "SEM_DADOS",
                "registros_processados": 0
            }

        # --------------------------------------------------
        # 8. SQL
        # --------------------------------------------------
        delete_sql = text("""
            DELETE FROM data_pr.his_selo_detalhe_pr
            WHERE contrato_id = :contrato_id
              AND sistema_origem_id = :sistema_origem_id
        """)

        insert_sql = text("""
            INSERT INTO data_pr.his_selo_detalhe_pr (
                recordnumber,
                selo_principal,
                selo_retificacao,
                selo_anulacao,
                selo_cancelamento,
                seloretificado,
                codtipoato,
                id_codigo_ato,
                numpedido,
                protocolo,
                documento,
                chavedigital,
                qrcode,
                caminhoimagem,
                json,
                valorbase,
                divisor,
                quantidade,
                funrejus,
                iss,
                fadep,
                funarpen,
                cartorio,
                distribuidor,
                contraente_nome,
                contraente_cpf,
                status,
                mensagem,
                id_tipo_gratuidade,
                id_usuario,
                contrato_id,
                sistema_origem_id
            ) VALUES (
                :recordnumber,
                :selo_principal,
                :selo_retificacao,
                :selo_anulacao,
                :selo_cancelamento,
                :seloretificado,
                :codtipoato,
                :id_codigo_ato,
                :numpedido,
                :protocolo,
                :documento,
                :chavedigital,
                :qrcode,
                :caminhoimagem,
                CAST(:json AS JSONB),
                :valorbase,
                :divisor,
                :quantidade,
                :funrejus,
                :iss,
                :fadep,
                :funarpen,
                :cartorio,
                :distribuidor,
                :contraente_nome,
                :contraente_cpf,
                :status,
                :mensagem,
                :id_tipo_gratuidade,
                :id_usuario,
                :contrato_id,
                :sistema_origem_id
            )
            ON CONFLICT (recordnumber, sistema_origem_id) DO NOTHING
        """)

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

        atualizar_log_importacao(
            log_id=log_id,
            status="SUCESSO",
            registros_processados=len(registros)
        )

        return {
            "status": "SUCESSO",
            "modo_importacao": modo_importacao.value,
            "registros_processados": len(registros)
        }

    except Exception as e:
        if log_id:
            atualizar_log_importacao(
                log_id=log_id,
                status="ERRO",
                mensagem=str(e)
            )
        raise
