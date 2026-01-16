import pandas as pd
from sqlalchemy import text
from app.core.database import engine


COLUNAS_ESPERADAS = {
    "codlcto",
    "descricao",
    "tipo_lanc",
    "grupodecontas",
    "status_inativo"
}


def importar_tabela_lancamentos_pr(file: str, contrato_id: str, usuario_email: str):
    # 1. Ler Excel
    df = pd.read_excel(file)
    df.columns = df.columns.str.lower()

    # 2. Validar colunas
    colunas_arquivo = set(df.columns)
    if colunas_arquivo != COLUNAS_ESPERADAS:
        faltantes = COLUNAS_ESPERADAS - colunas_arquivo
        extras = colunas_arquivo - COLUNAS_ESPERADAS

        erros = []
        if faltantes:
            erros.append(f"Colunas ausentes: {', '.join(faltantes)}")
        if extras:
            erros.append(f"Colunas extras: {', '.join(extras)}")

        raise ValueError(" | ".join(erros))

    # 3. NORMALIZAÇÕES CORRETAS (ORDEM IMPORTA)

    # 3.1 status_inativo → boolean seguro
    df["status_inativo"] = (
        df["status_inativo"]
        .fillna(False)
        .astype(bool)
    )

    # 3.2 FORÇAR tudo para object (ESSENCIAL)
    df = df.astype(object)

    # 3.3 Converter NaN → None (agora funciona)
    df = df.where(pd.notnull(df), None)

    # 4. SQL
    sql = text("""
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
        ON CONFLICT (codlcto) DO NOTHING
    """)

    # 5. Executar
    with engine.begin() as conn:
        for _, row in df.iterrows():
            conn.execute(sql, row.to_dict())

    return {
        "status": "SUCESSO",
        "registros_processados": len(df)
    }
