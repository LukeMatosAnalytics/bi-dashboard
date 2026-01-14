"""
Endpoints do Dashboard
"""
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from typing import Optional
import io
import csv

from app.core.auth import get_usuario_atual
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/selos-faltantes")
def get_selos_faltantes(
    data_inicio: Optional[str] = Query(None, description="Data início (YYYY-MM-DD)"),
    data_fim: Optional[str] = Query(None, description="Data fim (YYYY-MM-DD)"),
    contrato_id: Optional[str] = Query(None, description="ID do contrato (apenas MASTER)"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    usuario=Depends(get_usuario_atual)
):
    """
    Retorna selos que estão em his_selo_detalhe_pr mas NÃO estão em os_selo.
    Este é o indicador principal: selos baixados mas não enviados ao FNC.
    """
    # Se não for MASTER, força o contrato do usuário
    if usuario["role"] != "MASTER":
        contrato_id = usuario["contrato_id"]
    
    return DashboardService.get_selos_faltantes(
        contrato_id=contrato_id,
        data_inicio=data_inicio,
        data_fim=data_fim,
        page=page,
        limit=limit
    )


@router.get("/selos-faltantes/export")
def export_selos_faltantes(
    data_inicio: Optional[str] = Query(None),
    data_fim: Optional[str] = Query(None),
    contrato_id: Optional[str] = Query(None),
    usuario=Depends(get_usuario_atual)
):
    """
    Exporta lista completa de selos faltantes em CSV
    """
    if usuario["role"] != "MASTER":
        contrato_id = usuario["contrato_id"]
    
    dados = DashboardService.get_selos_faltantes_export(
        contrato_id=contrato_id,
        data_inicio=data_inicio,
        data_fim=data_fim
    )
    
    # Gera CSV
    output = io.StringIO()
    writer = csv.writer(output, delimiter=";")
    
    # Cabeçalho
    writer.writerow([
        "Código do Selo",
        "Cód. Tipo Ato",
        "Descrição do Ato",
        "Livro",
        "Folha",
        "Capa",
        "Data de Registro",
        "OS"
    ])
    
    # Dados
    for selo in dados:
        writer.writerow([
            selo.get("codigo_selo", ""),
            selo.get("cod_tipo_ato", ""),
            selo.get("descricao_tipo_ato", ""),
            selo.get("livro", ""),
            selo.get("folha", ""),
            selo.get("capa", ""),
            selo.get("data_ato", ""),
            selo.get("os", "")
        ])
    
    output.seek(0)
    
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=selos_faltantes.csv"
        }
    )


@router.get("/evolucao-mensal")
def get_evolucao_mensal(
    contrato_id: Optional[str] = Query(None),
    usuario=Depends(get_usuario_atual)
):
    """
    Retorna evolução mensal de selos faltantes
    """
    if usuario["role"] != "MASTER":
        contrato_id = usuario["contrato_id"]
    
    return DashboardService.get_evolucao_mensal(contrato_id=contrato_id)


@router.get("/resumo")
def get_resumo(
    contrato_id: Optional[str] = Query(None),
    usuario=Depends(get_usuario_atual)
):
    """
    Retorna resumo geral com KPIs principais
    """
    if usuario["role"] != "MASTER":
        contrato_id = usuario["contrato_id"]
    
    return DashboardService.get_resumo(contrato_id=contrato_id)
