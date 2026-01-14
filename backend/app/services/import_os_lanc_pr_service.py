import pandas as pd
from sqlalchemy import text
from app.core.database import engine

COLUNAS_ESPERADAS = {
    "id", "situacao", "quantidade", "valor",
    "capa", "livro", "folha",
    "dt_lancou", "os", "sequencia",
    "operacao", "lcto", "recibo"
}

def importar_os_lanc_pr(file, contrato_id, usuario_email):
    # 1. Ler Excel
    df = pd.read_excel(file)
    df.columns = df.columns.str.lower()

    # 2. Validar estrutura
    if set(df.columns) != COLUNAS_ESPERADAS:
        raise ValueError(
            f"Estrutura inválida. Esperado: {COLUNAS_ESPERADAS}"
        )

    # 3. Tratamentos obrigatórios
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    df["quantidade"] = pd.to_numeric(df["quantidade"], errors="coerce").fillna(1)

    df["valor_abs"] = df["valor"].abs()

    df["natureza"] = df["operacao"].map({
        "E": "ENTRADA",
        "S": "SAIDA"
    })

    df["data_lancamento_date"] = pd.to_datetime(
        df["dt_lancou"], errors="coerce"
    ).dt.date

    df["selo_principal"] = (
        "IDREF-" +
        df["capa"].fillna("") +
        df["livro"].fillna("") +
        df["folha"].fillna("")
    )

    # 4. SQL de inserção (seguro e idempotente)
    sql = text("""
        INSERT INTO data_pr.fato_os_lanc (
            contrato_id,
            id_origem,
            os,
            sequencia,
            situacao,
            lcto,
            quantidade,
            valor,
            valor_abs,
            operacao,
            natureza,
            capa,
            livro,
            folha,
            selo_principal,
            dt_lancou,
            data_lancamento_date,
            recibo
        ) VALUES (
            :contrato_id,
            :id,
            :os,
            :sequencia,
            :situacao,
            :lcto,
            :quantidade,
            :valor,
            :valor_abs,
            :operacao,
            :natureza,
            :capa,
            :livro,
            :folha,
            :selo_principal,
            :dt_lancou,
            :data_lancamento_date,
            :recibo
        )
        ON CONFLICT (contrato_id, os, sequencia) DO NOTHING
    """)

    # 5. Executar inserções
    with engine.begin() as conn:
        for _, row in df.iterrows():
            conn.execute(
                sql,
                {**row.to_dict(), "contrato_id": contrato_id}
            )
