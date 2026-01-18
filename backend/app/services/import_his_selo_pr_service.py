import os
import pandas as pd
from sqlalchemy import text

from app.core.database import engine
from app.core.import_config import TIPOS_IMPORTACAO, ModoImportacao
from app.core.security import verificar_senha_usuario
from app.core.import_log import registrar_import_log
from app.core.exceptions import BusinessException
from app.core.errors import ErrorCode


# ======================================================
# COLUNAS OBRIGATÓRIAS DO ARQUIVO HIS_SELO (EXCEL)
# ======================================================

COLUNAS_OBRIGATORIAS = {
    "id",
    "selo",
    "tipo_ato",
    "capa",
    "livro",
    "folha",
    "quantidade",
    "data",   # data do ato (BASE TEMPORAL)
}


# ======================================================
# SERVICE
# ======================================================

def importar_his_selo_pr(
    *,
    file: str,
    contrato_id: str,
    usuario_email: str,
    usuario_id: int,
    sistema_origem_id: int,
    modo_importacao: ModoImportacao,
    senha_confirmacao: str | None,
):
    registros_lidos = 0
    registros_processados = 0
    nome_arquivo = os.path.basename(file)

    try:
        # --------------------------------------------------
        # 1. Validar tipo de importação
        # --------------------------------------------------
        tipo = "his_selo"

        if tipo not in TIPOS_IMPORTACAO:
            raise BusinessException(
                ErrorCode.INVALID_IMPORT_MODE,
                detail=f"Tipo de importação não configurado: {tipo}"
            )

        config = TIPOS_IMPORTACAO[tipo]

        if (
            modo_importacao == ModoImportacao.INCREMENTAL
            and not config["permite_incremental"]
        ):
            raise BusinessException(
                ErrorCode.INVALID_IMPORT_MODE,
                detail="Carga incremental não permitida para este tipo"
            )

        # --------------------------------------------------
        # 2. Validar senha (somente INITIAL)
        # --------------------------------------------------
        if modo_importacao == ModoImportacao.INITIAL:
            if not senha_confirmacao:
                raise BusinessException(ErrorCode.INVALID_PASSWORD)

            if not verificar_senha_usuario(
                email=usuario_email,
                senha_plana=senha_confirmacao
            ):
                raise BusinessException(ErrorCode.INVALID_PASSWORD)

        # --------------------------------------------------
        # 3. Ler Excel
        # --------------------------------------------------
        df = pd.read_excel(file)
        df.columns = df.columns.str.lower()

        registros_lidos = len(df)

        if registros_lidos == 0:
            raise BusinessException(ErrorCode.EMPTY_FILE)

        # --------------------------------------------------
        # 4. Validar colunas obrigatórias
        # --------------------------------------------------
        faltantes = COLUNAS_OBRIGATORIAS - set(df.columns)

        if faltantes:
            raise BusinessException(
                ErrorCode.MISSING_REQUIRED_COLUMNS,
                detail=f"Colunas ausentes: {', '.join(sorted(faltantes))}"
            )

        # --------------------------------------------------
        # 5. Normalizações
        # --------------------------------------------------
        df = df[list(COLUNAS_OBRIGATORIAS)]
        df = df.astype(object)
        df = df.where(pd.notnull(df), None)

        df["quantidade"] = pd.to_numeric(
            df["quantidade"],
            errors="coerce"
        ).fillna(1)

        df["data"] = pd.to_datetime(
            df["data"],
            errors="coerce"
        )

        # --------------------------------------------------
        # 6. Remover registros inválidos
        # --------------------------------------------------
        df = df[
            df["selo"].notna()
            & df["data"].notna()
        ]

        if df.empty:
            raise BusinessException(
                ErrorCode.EMPTY_FILE,
                detail="Nenhum registro válido após validações"
            )

        # --------------------------------------------------
        # 7. Colunas de controle
        # --------------------------------------------------
        df["contrato_id"] = contrato_id
        df["sistema_origem_id"] = sistema_origem_id

        registros = df.to_dict("records")

        # --------------------------------------------------
        # 8. SQL DELETE (somente INITIAL)
        # --------------------------------------------------
        delete_sql = text("""
            DELETE FROM data_pr.his_selo
            WHERE contrato_id = :contrato_id
              AND sistema_origem_id = :sistema_origem_id
        """)

        # --------------------------------------------------
        # 9. SQL INSERT (APENAS COLUNAS EXISTENTES)
        # --------------------------------------------------
        insert_sql = text("""
            INSERT INTO data_pr.his_selo (
                id,
                selo,
                tipo_ato,
                capa,
                livro,
                folha,
                quantidade,
                data,
                contrato_id,
                sistema_origem_id
            ) VALUES (
                :id,
                :selo,
                :tipo_ato,
                :capa,
                :livro,
                :folha,
                :quantidade,
                :data,
                :contrato_id,
                :sistema_origem_id
            )
            ON CONFLICT (contrato_id, sistema_origem_id, id)
            DO NOTHING
        """)

        # --------------------------------------------------
        # 10. EXECUÇÃO
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

            result = conn.execute(insert_sql, registros)
            registros_processados = result.rowcount or 0

        # --------------------------------------------------
        # 11. LOG DE SUCESSO
        # --------------------------------------------------
        registrar_import_log(
            usuario_id=usuario_id,
            usuario_email=usuario_email,
            contrato_id=contrato_id,
            sistema_origem_id=sistema_origem_id,
            tipo_arquivo="his_selo",
            modo_importacao=modo_importacao.value,
            nome_arquivo=nome_arquivo,
            total_registros=registros_lidos,
            registros_processados=registros_processados,
            status="SUCCESS"
        )

        return {
            "success": True,
            "data": {
                "arquivo": nome_arquivo,
                "modo_importacao": modo_importacao.value,
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
            sistema_origem_id=sistema_origem_id,
            tipo_arquivo="his_selo",
            modo_importacao=modo_importacao.value,
            nome_arquivo=nome_arquivo,
            total_registros=registros_lidos,
            registros_processados=0,
            status="ERROR",
            mensagem=e.detail or e.message
        )
        raise

    # ==================================================
    # ERROS INESPERADOS
    # ==================================================
    except Exception as e:
        registrar_import_log(
            usuario_id=usuario_id,
            usuario_email=usuario_email,
            contrato_id=contrato_id,
            sistema_origem_id=sistema_origem_id,
            tipo_arquivo="his_selo",
            modo_importacao=modo_importacao.value,
            nome_arquivo=nome_arquivo,
            total_registros=registros_lidos,
            registros_processados=0,
            status="ERROR",
            mensagem=str(e)
        )
        raise
