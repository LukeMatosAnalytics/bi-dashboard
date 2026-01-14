"""
Serviço de Importação de Arquivos Excel
"""
import os
import pandas as pd
from typing import Dict, Any
from fastapi import HTTPException
from sqlalchemy import text

from app.core.database import engine
from app.services.import_log_service import registrar_importacao

SCHEMA_PR = "data_pr"

# Mapeamento de colunas esperadas por tipo de arquivo
# Baseado nos arquivos Excel reais do projeto
COLUNAS_ESPERADAS = {
    "os_selo": {
        "id", "os", "selo"  # Colunas mínimas
    },
    "os_lanc": {
        "id", "situacao", "quantidade", "valor",
        "capa", "livro", "folha", "dt_lancou",
        "os", "sequencia", "operacao", "lcto", "recibo"
    },
    "his_selo": {
        "id", "selo", "data", "tipo_ato"  # Colunas mínimas
    },
    "his_selo_detalhe_pr": {
        "id", "selo_principal", "codtipoato", "dataato"  # Colunas mínimas
    },
    "tabela_de_lancamentos": {
        "codlcto", "descricao"  # Colunas mínimas
    }
}

# Mapeamento de tabelas
TABELA_MAP = {
    "os_selo": "os_selo",
    "os_lanc": "fato_os_lanc",
    "his_selo": "his_selo",
    "his_selo_detalhe_pr": "his_selo_detalhe_pr",
    "tabela_de_lancamentos": "tabela_de_lancamentos"
}


class ImportService:
    """
    Serviço para importação de arquivos Excel
    """
    
    @staticmethod
    def importar_arquivo(
        caminho_excel: str,
        tipo_arquivo: str,
        contrato_id: str,
        email_usuario: str,
        nome_arquivo: str,
        chunk_size: int = 5000
    ) -> Dict[str, Any]:
        """
        Importa arquivo Excel para o banco de dados
        """
        try:
            # Lê Excel
            df = pd.read_excel(caminho_excel)
            df.columns = [c.strip().lower() for c in df.columns]
            
            # Valida colunas mínimas (verifica se as esperadas estão presentes)
            colunas_esperadas = COLUNAS_ESPERADAS.get(tipo_arquivo, set())
            colunas_arquivo = set(df.columns)
            
            faltando = colunas_esperadas - colunas_arquivo
            if faltando:
                raise ValueError(f"Colunas ausentes: {', '.join(faltando)}")
            
            # Adiciona contrato_id
            df["contrato_id"] = contrato_id
            
            # Processa de acordo com o tipo
            if tipo_arquivo == "os_lanc":
                total = ImportService._importar_os_lanc(df, contrato_id)
            elif tipo_arquivo == "os_selo":
                total = ImportService._importar_os_selo(df, contrato_id)
            elif tipo_arquivo == "his_selo":
                total = ImportService._importar_his_selo(df, contrato_id)
            elif tipo_arquivo == "his_selo_detalhe_pr":
                total = ImportService._importar_his_selo_detalhe(df, contrato_id)
            elif tipo_arquivo == "tabela_de_lancamentos":
                total = ImportService._importar_tabela_lancamentos(df, contrato_id)
            else:
                raise ValueError(f"Tipo de arquivo não suportado: {tipo_arquivo}")
            
            # Registra log de sucesso
            registrar_importacao(
                contrato_id=contrato_id,
                email_usuario=email_usuario,
                nome_arquivo=nome_arquivo,
                tipo_arquivo=tipo_arquivo,
                quantidade_registros=total,
                status="SUCESSO"
            )
            
            return {
                "mensagem": "Importação concluída com sucesso",
                "registros_processados": total,
                "tipo_arquivo": tipo_arquivo
            }
            
        except Exception as erro:
            # Registra log de erro
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
            # Remove arquivo temporário
            if os.path.exists(caminho_excel):
                os.remove(caminho_excel)
    
    @staticmethod
    def _importar_os_lanc(df: pd.DataFrame, contrato_id: str) -> int:
        """
        Importa dados de OS x Lançamentos
        """
        # Tratamentos
        df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
        df["quantidade"] = pd.to_numeric(df["quantidade"], errors="coerce").fillna(1)
        df["valor_abs"] = df["valor"].abs()
        df["natureza"] = df["operacao"].map({"E": "ENTRADA", "S": "SAIDA"})
        df["data_lancamento_date"] = pd.to_datetime(df["dt_lancou"], errors="coerce").dt.date
        df["selo_principal"] = "IDREF-" + df["capa"].fillna("").astype(str) + df["livro"].fillna("").astype(str) + df["folha"].fillna("").astype(str)
        
        sql = text("""
        INSERT INTO data_pr.fato_os_lanc (
            contrato_id, id_origem, os, sequencia, situacao, lcto,
            quantidade, valor, valor_abs, operacao, natureza,
            capa, livro, folha, selo_principal, dt_lancou,
            data_lancamento_date, recibo
        ) VALUES (
            :contrato_id, :id, :os, :sequencia, :situacao, :lcto,
            :quantidade, :valor, :valor_abs, :operacao, :natureza,
            :capa, :livro, :folha, :selo_principal, :dt_lancou,
            :data_lancamento_date, :recibo
        )
        ON CONFLICT (contrato_id, os, sequencia) DO UPDATE SET
            situacao = EXCLUDED.situacao,
            valor = EXCLUDED.valor,
            valor_abs = EXCLUDED.valor_abs
        """)
        
        total = 0
        with engine.begin() as conn:
            for _, row in df.iterrows():
                conn.execute(sql, {**row.to_dict(), "contrato_id": contrato_id})
                total += 1
        
        return total
    
    @staticmethod
    def _importar_os_selo(df: pd.DataFrame, contrato_id: str) -> int:
        """
        Importa dados de OS x Selo
        """
        sql = text("""
        INSERT INTO data_pr.os_selo (contrato_id, id_origem, os, codigo_selo)
        VALUES (:contrato_id, :id, :os, :selo)
        ON CONFLICT (contrato_id, os, codigo_selo) DO NOTHING
        """)
        
        total = 0
        with engine.begin() as conn:
            for _, row in df.iterrows():
                conn.execute(sql, {
                    "contrato_id": contrato_id,
                    "id": str(row.get("id", "")),
                    "os": str(row.get("os", "")),
                    "selo": str(row.get("selo", ""))
                })
                total += 1
        
        return total
    
    @staticmethod
    def _importar_his_selo(df: pd.DataFrame, contrato_id: str) -> int:
        """
        Importa histórico de selos
        """
        # Pega todas as colunas disponíveis
        colunas_db = [
            "contrato_id", "id_origem", "auto_inc", "ativ_sel", "data", "hora",
            "operador", "tipo_ato", "capa", "livro", "folha", "servico",
            "tipo_his", "tipo_selo", "selo", "validador", "qtd", "data_envio",
            "data_compra", "finalizado", "baixado_postgres", "data_locacao",
            "hora_locacao", "id_status", "id_natureza_funapen", "id_usuario",
            "numero_pedido", "tem_erro"
        ]
        
        total = 0
        with engine.begin() as conn:
            for _, row in df.iterrows():
                params = {"contrato_id": contrato_id, "id_origem": str(row.get("id", ""))}
                
                # Mapeia colunas do Excel para colunas do banco
                if "selo" in row:
                    params["selo"] = str(row["selo"])
                if "data" in row:
                    params["data"] = row["data"]
                if "tipo_ato" in row:
                    params["tipo_ato"] = str(row["tipo_ato"])
                if "capa" in row:
                    params["capa"] = str(row.get("capa", ""))
                if "livro" in row:
                    params["livro"] = str(row.get("livro", ""))
                if "folha" in row:
                    params["folha"] = str(row.get("folha", ""))
                if "ativ_sel" in row:
                    params["ativ_sel"] = str(row.get("ativ_sel", ""))
                
                # SQL dinâmico baseado nos parâmetros disponíveis
                campos = ", ".join(params.keys())
                valores = ", ".join([f":{k}" for k in params.keys()])
                
                sql = text(f"""
                INSERT INTO data_pr.his_selo ({campos})
                VALUES ({valores})
                """)
                
                conn.execute(sql, params)
                total += 1
        
        return total
    
    @staticmethod
    def _importar_his_selo_detalhe(df: pd.DataFrame, contrato_id: str) -> int:
        """
        Importa histórico de selo detalhe PR
        """
        # Renomeia colunas para o padrão do banco
        df = df.rename(columns={
            "codtipoato": "cod_tipo_ato",
            "dataato": "data_ato",
            "numpedido": "num_pedido",
            "chavedigital": "chave_digital",
            "seloretificado": "selo_retificado",
            "valorbase": "valor_base",
            "recordnumber": "record_number",
            "selo_principal": "selo_principal"
        })
        
        total = 0
        with engine.begin() as conn:
            for _, row in df.iterrows():
                params = {
                    "contrato_id": contrato_id,
                    "id_origem": str(row.get("id", "")),
                    "selo_principal": str(row.get("selo_principal", "")),
                    "cod_tipo_ato": int(row["cod_tipo_ato"]) if pd.notna(row.get("cod_tipo_ato")) else None,
                    "data_ato": row.get("data_ato"),
                    "num_pedido": str(row.get("num_pedido", "")) if pd.notna(row.get("num_pedido")) else None,
                    "protocolo": str(row.get("protocolo", "")) if pd.notna(row.get("protocolo")) else None,
                    "documento": str(row.get("documento", "")) if pd.notna(row.get("documento")) else None,
                    "valor_base": float(row["valor_base"]) if pd.notna(row.get("valor_base")) else None,
                    "quantidade": int(row["quantidade"]) if pd.notna(row.get("quantidade")) else None,
                    "status": int(row["status"]) if pd.notna(row.get("status")) else None
                }
                
                sql = text("""
                INSERT INTO data_pr.his_selo_detalhe_pr (
                    contrato_id, id_origem, selo_principal, cod_tipo_ato,
                    data_ato, num_pedido, protocolo, documento,
                    valor_base, quantidade, status
                ) VALUES (
                    :contrato_id, :id_origem, :selo_principal, :cod_tipo_ato,
                    :data_ato, :num_pedido, :protocolo, :documento,
                    :valor_base, :quantidade, :status
                )
                """)
                
                conn.execute(sql, params)
                total += 1
        
        return total
    
    @staticmethod
    def _importar_tabela_lancamentos(df: pd.DataFrame, contrato_id: str) -> int:
        """
        Importa tabela de referência de lançamentos
        """
        sql = text("""
        INSERT INTO data_pr.tabela_de_lancamentos (
            contrato_id, codlcto, descricao, tipo_lanc, grupo_de_contas
        ) VALUES (
            :contrato_id, :codlcto, :descricao, :tipo_lanc, :grupo_de_contas
        )
        ON CONFLICT (contrato_id, codlcto) DO UPDATE SET
            descricao = EXCLUDED.descricao
        """)
        
        total = 0
        with engine.begin() as conn:
            for _, row in df.iterrows():
                conn.execute(sql, {
                    "contrato_id": contrato_id,
                    "codlcto": str(row.get("codlcto", "")),
                    "descricao": str(row.get("descricao", "")),
                    "tipo_lanc": str(row.get("tipo_lanc", "")) if pd.notna(row.get("tipo_lanc")) else None,
                    "grupo_de_contas": str(row.get("grupo_de_contas", "")) if pd.notna(row.get("grupo_de_contas")) else None
                })
                total += 1
        
        return total
