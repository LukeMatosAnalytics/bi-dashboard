import os
import pandas as pd
from sqlalchemy import text

from app.core.database import engine
from app.core.import_log import registrar_import_log
from app.core.exceptions import BusinessException
from app.core.errors import ErrorCode


# ======================================================
# COLUNAS OBRIGATÓRIAS DO ARQUIVO TABELA_LANCAMENTOS
# ======================================================

COLUNAS_OBRIGATORIAS = {
    "codlcto",
    "descricao",
    "tipo_lanc",
    "grupodecontas",
    "status_inativo",
}


# ======================================================
# SERVICE
# ======================================================

def importar_tabela_lancamentos_pr(
    *,
    file: str,
    contrato_id: str,
    usuario_email: str,
    usuario_id: int,
):
    nome_arquivo = os.path.basename(file)
    registros_lidos = 0
    registros_processados = 0

    try:
        # --------------------------------------------------
        # 1. Ler Excel
        # --------------------------------------------------
        df = pd.read_excel(file)
        df.columns = df.columns.str.lower()
        registros_lidos = len(df)

        if registros_lidos == 0:
            raise BusinessException(ErrorCode.EMPTY_FILE)

        # --------------------------------------------------
        # 2. Validar colunas obrigatórias
        # --------------------------------------------------
        colunas_arquivo = set(df.columns)
        faltantes = COLUNAS_OBRIGATORIAS - colunas_arquivo
        extras = colunas_arquivo - COLUNAS_OBRIGATORIAS

        if faltantes or extras:
            detalhe = []

            if faltantes:
                detalhe.append(
                    f"Colunas ausentes: {', '.join(sorted(faltantes))}"
                )
            if extras:
                detalhe.append(
                    f"Colunas extras: {', '.join(sorted(extras))}"
                )

            raise BusinessException(
                ErrorCode.MISSING_REQUIRED_COLUMNS,
                detail=" | ".join(detalhe)
            )

        # --------------------------------------------------
        # 3. Manter apenas colunas esperadas
        # --------------------------------------------------
        df = df[list(COLUNAS_OBRIGATORIAS)]

        # --------------------------------------------------
        # 4. Normalizações
        # --------------------------------------------------
        df["status_inativo"] = (
            df["status_inativo"]
            .fillna(False)
            .astype(bool)
        )

        df = df.astype(object)
        df = df.where(pd.notnull(df), None)

        # --------------------------------------------------
        # 5. SQL INSERT (dimensão – idempotente)
        # --------------------------------------------------
        insert_sql = text("""
            INSERT INTO data_pr.tipo_lancamento (
                codlcto,
                descricao,
                tipo_lanc,
                grupodecontas,
                status_inativo
            ) VALUES (
                :codlcto,
                :descricao,
                :tipo_lanc,
                :grupodecontas,
                :status_inativo
            )
            ON CONFLICT (codlcto)
            DO NOTHING
        """)

        # --------------------------------------------------
        # 6. EXECUÇÃO
        # --------------------------------------------------
        registros = df.to_dict("records")

        with engine.begin() as conn:
            result = conn.execute(insert_sql, registros)
            registros_processados = result.rowcount or 0

        # --------------------------------------------------
        # 7. LOG DE SUCESSO
        # --------------------------------------------------
        registrar_import_log(
            usuario_id=usuario_id,
            usuario_email=usuario_email,
            contrato_id=contrato_id,
            sistema_origem_id=None,
            tipo_arquivo="tabela_lancamentos",
            modo_importacao="INITIAL",
            nome_arquivo=nome_arquivo,
            total_registros=registros_lidos,
            registros_processados=registros_processados,
            status="SUCCESS"
        )

        return {
            "success": True,
            "data": {
                "arquivo": nome_arquivo,
                "modo_importacao": "INITIAL",
                "registros_lidos": registros_lidos,
                "registros_processados": registros_processados
            }
        }

    # ==================================================
    # ERROS DE NEGÓCIO
    # ==================================================
    except BusinessException as e:
        registrar_import_log(
            usuario_id=usuario_id,
            usuario_email=usuario_email,
            contrato_id=contrato_id,
            sistema_origem_id=None,
            tipo_arquivo="tabela_lancamentos",
            modo_importacao="INITIAL",
            nome_arquivo=nome_arquivo,
            total_registros=registros_lidos,
            registros_processados=0,
            status="ERROR",
            mensagem=e.detail or e.message
        )
        raise

    # ==================================================
    # ERROS NÃO MAPEADOS
    # ==================================================
    except Exception as e:
        registrar_import_log(
            usuario_id=usuario_id,
            usuario_email=usuario_email,
            contrato_id=contrato_id,
            sistema_origem_id=None,
            tipo_arquivo="tabela_lancamentos",
            modo_importacao="INITIAL",
            nome_arquivo=nome_arquivo,
            total_registros=registros_lidos,
            registros_processados=0,
            status="ERROR",
            mensagem=str(e)
        )
        raise
