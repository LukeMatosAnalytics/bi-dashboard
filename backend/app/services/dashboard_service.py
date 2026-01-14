"""
Serviço de Dashboard - Lógica de negócio para indicadores
"""
from typing import Optional, List, Dict, Any
from sqlalchemy import text
from app.core.database import engine

# Mapeamento de Códigos de Ato FUNARPEN - Instrução Normativa 019/2023
TIPOS_ATO_FUNARPEN = {
    # REGISTRO CIVIL - Nascimento
    101: 'Nascimento - Registro',
    102: 'Nascimento - 2ª Via',
    103: 'Nascimento - Averbação',
    104: 'Nascimento - Busca',
    105: 'Nascimento - Certidão Inteiro Teor',
    # REGISTRO CIVIL - Casamento
    111: 'Casamento - Habilitação',
    112: 'Casamento - Registro',
    116: 'Casamento - Certidão',
    117: 'Casamento - 2ª Via',
    118: 'Casamento - Averbação',
    119: 'Casamento - Busca',
    120: 'Casamento - Certidão Inteiro Teor',
    121: 'Casamento - Proclamas',
    122: 'Casamento - Conversão União Estável',
    123: 'Casamento - Celebração',
    124: 'Casamento - Separação/Divórcio',
    125: 'Casamento - Restabelecimento Sociedade Conjugal',
    126: 'Casamento - Alteração Regime de Bens',
    127: 'Casamento - Escritura Pública',
    # REGISTRO CIVIL - Óbito
    130: 'Óbito - Registro',
    134: 'Óbito - 2ª Via',
    135: 'Óbito - Certidão Inteiro Teor',
    # TABELIONATO DE NOTAS
    402: 'Escritura Pública',
    403: 'Procuração',
    404: 'Substabelecimento',
    408: 'Ata Notarial',
    409: 'Testamento',
    410: 'Aprovação de Testamento',
    412: 'Autenticação',
    418: 'Reconhecimento de Firma',
    419: 'Abertura de Firma',
    420: 'Certidão',
    421: 'Apostilamento',
    422: 'Diligência',
    424: 'Traslado',
    425: 'Cópia Autenticada',
    427: 'Revogação de Procuração',
    430: 'Inventário Extrajudicial',
    431: 'Divórcio Extrajudicial',
    432: 'Separação Extrajudicial',
    433: 'União Estável',
    435: 'Usucapião Extrajudicial',
    436: 'Declaração de Bens',
    437: 'Declaração Diversa',
    439: 'Emancipação',
    443: 'Notificação',
    447: 'Doação',
    449: 'Compra e Venda',
    450: 'Permuta',
}


class DashboardService:
    """
    Serviço para consultas de dashboard e indicadores
    """
    
    @staticmethod
    def get_selos_faltantes(
        contrato_id: Optional[str] = None,
        data_inicio: Optional[str] = None,
        data_fim: Optional[str] = None,
        page: int = 1,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        Retorna selos que estão em his_selo_detalhe_pr mas NÃO em os_selo.
        Este é o indicador principal: selos baixados não enviados ao FNC.
        """
        offset = (page - 1) * limit
        
        # Constrói cláusula WHERE dinâmica
        where_clauses = ["os.codigo_selo IS NULL"]
        params = {}
        
        if contrato_id:
            where_clauses.append("hsd.contrato_id = :contrato_id")
            params["contrato_id"] = contrato_id
        
        if data_inicio:
            where_clauses.append("hsd.data_ato >= :data_inicio")
            params["data_inicio"] = data_inicio
        
        if data_fim:
            where_clauses.append("hsd.data_ato <= :data_fim")
            params["data_fim"] = data_fim
        
        where_string = " AND ".join(where_clauses)
        
        # Query de contagem
        count_sql = f"""
        SELECT COUNT(DISTINCT hsd.selo_principal) as total
        FROM data_pr.his_selo_detalhe_pr hsd
        LEFT JOIN data_pr.os_selo os 
            ON hsd.selo_principal = os.codigo_selo 
            AND hsd.contrato_id = os.contrato_id
        WHERE {where_string}
        """
        
        # Query de dados
        data_sql = f"""
        SELECT DISTINCT ON (hsd.selo_principal)
            hsd.selo_principal as codigo_selo,
            hsd.cod_tipo_ato,
            hs.livro,
            hs.folha,
            hs.capa,
            hsd.data_ato,
            hs.ativ_sel as os
        FROM data_pr.his_selo_detalhe_pr hsd
        LEFT JOIN data_pr.os_selo os 
            ON hsd.selo_principal = os.codigo_selo 
            AND hsd.contrato_id = os.contrato_id
        LEFT JOIN data_pr.his_selo hs 
            ON hsd.selo_principal = hs.selo 
            AND hsd.contrato_id = hs.contrato_id
        WHERE {where_string}
        ORDER BY hsd.selo_principal, hsd.data_ato DESC
        LIMIT :limit OFFSET :offset
        """
        
        params["limit"] = limit
        params["offset"] = offset
        
        with engine.connect() as conn:
            # Conta total
            count_result = conn.execute(text(count_sql), params).first()
            total = count_result[0] if count_result else 0
            
            # Busca dados
            data_result = conn.execute(text(data_sql), params).mappings().all()
        
        # Processa resultados adicionando descrição do tipo de ato
        selos = []
        for row in data_result:
            selo = dict(row)
            cod_tipo = selo.get("cod_tipo_ato")
            selo["descricao_tipo_ato"] = TIPOS_ATO_FUNARPEN.get(
                cod_tipo, f"Código {cod_tipo}" if cod_tipo else None
            )
            selos.append(selo)
        
        total_pages = (total + limit - 1) // limit
        
        return {
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": total_pages,
            "data": selos
        }
    
    @staticmethod
    def get_selos_faltantes_export(
        contrato_id: Optional[str] = None,
        data_inicio: Optional[str] = None,
        data_fim: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retorna todos os selos faltantes para exportação (sem paginação)
        """
        where_clauses = ["os.codigo_selo IS NULL"]
        params = {}
        
        if contrato_id:
            where_clauses.append("hsd.contrato_id = :contrato_id")
            params["contrato_id"] = contrato_id
        
        if data_inicio:
            where_clauses.append("hsd.data_ato >= :data_inicio")
            params["data_inicio"] = data_inicio
        
        if data_fim:
            where_clauses.append("hsd.data_ato <= :data_fim")
            params["data_fim"] = data_fim
        
        where_string = " AND ".join(where_clauses)
        
        sql = f"""
        SELECT DISTINCT ON (hsd.selo_principal)
            hsd.selo_principal as codigo_selo,
            hsd.cod_tipo_ato,
            hs.livro,
            hs.folha,
            hs.capa,
            hsd.data_ato,
            hs.ativ_sel as os
        FROM data_pr.his_selo_detalhe_pr hsd
        LEFT JOIN data_pr.os_selo os 
            ON hsd.selo_principal = os.codigo_selo 
            AND hsd.contrato_id = os.contrato_id
        LEFT JOIN data_pr.his_selo hs 
            ON hsd.selo_principal = hs.selo 
            AND hsd.contrato_id = hs.contrato_id
        WHERE {where_string}
        ORDER BY hsd.selo_principal, hsd.data_ato DESC
        """
        
        with engine.connect() as conn:
            result = conn.execute(text(sql), params).mappings().all()
        
        selos = []
        for row in result:
            selo = dict(row)
            cod_tipo = selo.get("cod_tipo_ato")
            selo["descricao_tipo_ato"] = TIPOS_ATO_FUNARPEN.get(
                cod_tipo, f"Código {cod_tipo}" if cod_tipo else None
            )
            selos.append(selo)
        
        return selos
    
    @staticmethod
    def get_evolucao_mensal(
        contrato_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retorna evolução mensal de selos faltantes
        """
        where_clauses = ["os.codigo_selo IS NULL", "hsd.data_ato IS NOT NULL"]
        params = {}
        
        if contrato_id:
            where_clauses.append("hsd.contrato_id = :contrato_id")
            params["contrato_id"] = contrato_id
        
        where_string = " AND ".join(where_clauses)
        
        sql = f"""
        SELECT 
            TO_CHAR(hsd.data_ato, 'YYYY-MM') as mes,
            COUNT(DISTINCT hsd.selo_principal) as quantidade
        FROM data_pr.his_selo_detalhe_pr hsd
        LEFT JOIN data_pr.os_selo os 
            ON hsd.selo_principal = os.codigo_selo 
            AND hsd.contrato_id = os.contrato_id
        WHERE {where_string}
        GROUP BY TO_CHAR(hsd.data_ato, 'YYYY-MM')
        ORDER BY mes
        """
        
        with engine.connect() as conn:
            result = conn.execute(text(sql), params).mappings().all()
        
        return [dict(r) for r in result]
    
    @staticmethod
    def get_resumo(contrato_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Retorna resumo geral com KPIs principais
        """
        params = {}
        contrato_filter = ""
        
        if contrato_id:
            contrato_filter = "WHERE contrato_id = :contrato_id"
            params["contrato_id"] = contrato_id
        
        # Total de selos faltantes
        sql_faltantes = f"""
        SELECT COUNT(DISTINCT hsd.selo_principal) as total
        FROM data_pr.his_selo_detalhe_pr hsd
        LEFT JOIN data_pr.os_selo os 
            ON hsd.selo_principal = os.codigo_selo 
            AND hsd.contrato_id = os.contrato_id
        WHERE os.codigo_selo IS NULL
        {('AND hsd.contrato_id = :contrato_id' if contrato_id else '')}
        """
        
        # Total de OS
        sql_os = f"""
        SELECT COUNT(DISTINCT os) as total
        FROM data_pr.fato_os_lanc
        {contrato_filter}
        """
        
        # Total de selos em os_selo
        sql_selos = f"""
        SELECT COUNT(*) as total
        FROM data_pr.os_selo
        {contrato_filter}
        """
        
        with engine.connect() as conn:
            faltantes = conn.execute(text(sql_faltantes), params).first()
            total_os = conn.execute(text(sql_os), params).first()
            total_selos = conn.execute(text(sql_selos), params).first()
        
        return {
            "selos_faltantes": faltantes[0] if faltantes else 0,
            "total_os": total_os[0] if total_os else 0,
            "total_selos_os_selo": total_selos[0] if total_selos else 0
        }
