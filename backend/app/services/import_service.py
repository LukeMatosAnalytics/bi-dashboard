import pandas as pd
import os
from sqlalchemy import text
from fastapi import HTTPException

from app.core.database import engine
from app.services.import_log_service import registrar_importacao


SCHEMA_PR = "data_pr"

COLUNAS_MAP = {
    "os_selo": {"id", "os_id", "selo", "quantidade"},
    "os_lanc": {"id", "os_id", "data", "valor", "descricao"},
    "his_selo": {"id", "selo", "data", "tipo_ato"},
    "tabela_de_lancamentos": {"id", "data", "tipo", "valor"},
}


def importar_em_chunks(
    caminho_excel: str,
    tabela: str,
    contrato_id: str,
    email_usuario: str,
    nome_arquivo: str,
    tipo_arquivo: str,
    chunk_size: int = 10000
):
    colunas_esperadas = COLUNAS_MAP[tipo_arquivo]

    caminho_csv = caminho_excel.replace(".xlsx", ".csv")

    try:
        # 1️⃣ Converter Excel → CSV (uma vez)
        df_excel = pd.read_excel(caminho_excel)
        df_excel.to_csv(caminho_csv, index=False)

        total = 0

        # 2️⃣ Ler CSV em chunks
        for df in pd.read_csv(caminho_csv, chunksize=chunk_size):
            df.columns = [c.strip().lower() for c in df.columns]

            colunas = set(df.columns)

            faltando = colunas_esperadas - colunas
            extras = colunas - colunas_esperadas

            if faltando:
                raise ValueError(f"Colunas ausentes: {', '.join(faltando)}")
            if extras:
                raise ValueError(f"Colunas não esperadas: {', '.join(extras)}")

            if not pd.api.types.is_numeric_dtype(df["id"]):
                raise ValueError("Coluna 'id' deve ser numérica")

            df["contrato_id"] = contrato_id

            campos = [c for c in df.columns if c != "id"]
            campos_insert = ", ".join(campos)
            valores = ", ".join([f":{c}" for c in campos])
            updates = ", ".join([f"{c} = EXCLUDED.{c}" for c in campos])

            sql = f"""
            INSERT INTO {SCHEMA_PR}.{tabela} (
                id, {campos_insert}
            )
            VALUES (
                :id, {valores}
            )
            ON CONFLICT (id)
            DO UPDATE SET {updates}
            """

            registros = df.to_dict(orient="records")

            with engine.begin() as conn:
                conn.execute(text(sql), registros)

            total += len(df)

        registrar_importacao(
            contrato_id=contrato_id,
            email_usuario=email_usuario,
            nome_arquivo=nome_arquivo,
            tipo_arquivo=tipo_arquivo,
            quantidade_registros=total,
            status="SUCESSO"
        )

        return {
            "mensagem": "Importação concluída",
            "registros_processados": total
        }

    except Exception as erro:
        registrar_importacao(
            contrato_id=contrato_id,
            email_usuario=email_usuario,
            nome_arquivo=nome_arquivo,
            tipo_arquivo=tipo_arquivo,
            quantidade_registros=None,
            status="ERRO",
            mensagem_erro=str(erro)
        )
        raise HTTPException(status_code=400, detail=str(erro))

    finally:
        if os.path.exists(caminho_csv):
            os.remove(caminho_csv)
