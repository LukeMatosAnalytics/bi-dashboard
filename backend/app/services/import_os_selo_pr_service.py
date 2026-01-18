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
# COLUNAS OBRIGATÓRIAS DO ARQUIVO OS_SELO
# ======================================================

COLUNAS_OBRIGATORIAS = {
    "id",
    "os_id",
    "selo",
    "quantidade",
}


# ======================================================
# SERVICE
# ======================================================

def importar_os_selo_pr(
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
    tipo_arquivo = "os_selo"

    # --------------------------------------------------
    # 1. Validação de configuração
    # --------------------------------------------------
    if tipo_arquivo not in TIPOS_IMPORTACAO:
        raise BusinessException(
            error_code=ErrorCode.INVALID_IMPORT_MODE,
            detail=f"Tipo de importação não configurado: {tipo_arquivo}"
        )

    config = TIPOS_IMPORTACAO[tipo_arquivo]

    if (
        modo_importacao == ModoImportacao.INCREMENTAL
        and not config["permite_incremental"]
    ):
        raise BusinessException(
            error_code=ErrorCode.INVALID_IMPORT_MODE
        )

    # --------------------------------------------------
    # 2. Validação de senha (somente INITIAL)
    # --------------------------------------------------
    if modo_importacao == ModoImportacao.INITIAL:
        if not senha_confirmacao or not verificar_senha_usuario(
            email=usuario_email,
            senha_plana=senha_confirmacao
        ):
            raise BusinessException(
                error_code=ErrorCode.INVALID_PASSWORD
            )

    # --------------------------------------------------
    # 3. Leitura do arquivo
    # --------------------------------------------------
    df = pd.read_excel(file)
    df.columns = df.columns.str.lower()
    registros_lidos = len(df)

    if registros_lidos == 0:
        raise BusinessException(
            error_code=ErrorCode.EMPTY_FILE
        )

    # --------------------------------------------------
    # 4. Validação de colunas
    # --------------------------------------------------
    faltantes = COLUNAS_OBRIGATORIAS - set(df.columns)
    if faltantes:
        raise BusinessException(
            error_code=ErrorCode.MISSING_REQUIRED_COLUMNS,
            detail=f"Colunas ausentes: {', '.join(sorted(faltantes))}"
        )

    # --------------------------------------------------
    # 5. Seleção e normalização
    # --------------------------------------------------
    df = df[list(COLUNAS_OBRIGATORIAS)]
    df = df.astype(object)
    df = df.where(pd.notnull(df), None)

    df["quantidade"] = (
        pd.to_numeric(df["quantidade"], errors="coerce")
        .fillna(1)
    )

    # --------------------------------------------------
    # 6. Remoção de registros inválidos
    # --------------------------------------------------
    df = df[
        df["os_id"].notna()
        & df["selo"].notna()
    ]

    if df.empty:
        raise BusinessException(
            error_code=ErrorCode.EMPTY_FILE,
            detail="Nenhum registro válido após validações"
        )

    # --------------------------------------------------
    # 7. Colunas de controle
    # --------------------------------------------------
    df["contrato_id"] = contrato_id
    df["sistema_origem_id"] = sistema_origem_id
    registros = df.to_dict("records")

    # --------------------------------------------------
    # 8. SQL
    # --------------------------------------------------
    delete_sql = text("""
        DELETE FROM data_pr.os_selo
        WHERE contrato_id = :contrato_id
          AND sistema_origem_id = :sistema_origem_id
    """)

    insert_sql = text("""
        INSERT INTO data_pr.os_selo (
            id,
            os_id,
            selo,
            quantidade,
            contrato_id,
            sistema_origem_id
        ) VALUES (
            :id,
            :os_id,
            :selo,
            :quantidade,
            :contrato_id,
            :sistema_origem_id
        )
        ON CONFLICT (contrato_id, sistema_origem_id, os_id, selo)
        DO NOTHING
    """)

    # --------------------------------------------------
    # 9. Execução
    # --------------------------------------------------
    with engine.begin() as conn:
        if modo_importacao == ModoImportacao.INITIAL:
            conn.execute(
                delete_sql,
                {
                    "contrato_id": contrato_id,
                    "sistema_origem_id": sistema_origem_id,
                }
            )

        result = conn.execute(insert_sql, registros)
        registros_processados = result.rowcount or 0

    # --------------------------------------------------
    # 10. Log de sucesso
    # --------------------------------------------------
    registrar_import_log(
        usuario_id=usuario_id,
        usuario_email=usuario_email,
        contrato_id=contrato_id,
        sistema_origem_id=sistema_origem_id,
        tipo_arquivo=tipo_arquivo,
        modo_importacao=modo_importacao.value,
        nome_arquivo=nome_arquivo,
        total_registros=registros_lidos,
        registros_processados=registros_processados,
        status="SUCCESS",
    )

    return {
        "success": True,
        "data": {
            "arquivo": nome_arquivo,
            "modo_importacao": modo_importacao.value,
            "registros_lidos": registros_lidos,
            "registros_processados": registros_processados,
        }
    }
