"""
Endpoints de importação de dados - Estado PR
"""
import os
import shutil
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException

from app.core.permissions import somente_admin_ou_master
from app.services.import_service import ImportService

router = APIRouter(prefix="/import/pr", tags=["Importação PR"])

TEMP_FOLDER = "temp"


def _salvar_arquivo_temporario(arquivo: UploadFile) -> str:
    """Salva arquivo em pasta temporária"""
    os.makedirs(TEMP_FOLDER, exist_ok=True)
    caminho = os.path.join(TEMP_FOLDER, arquivo.filename)
    
    with open(caminho, "wb") as buffer:
        shutil.copyfileobj(arquivo.file, buffer)
    
    return caminho


def _validar_nome_arquivo(nome: str, contrato_id: str):
    """Valida que arquivo pertence ao contrato do usuário"""
    if not nome.lower().endswith(".xlsx"):
        raise HTTPException(400, "Arquivo deve ser .xlsx")
    
    if not nome.startswith(contrato_id):
        raise HTTPException(
            403,
            f"Arquivo deve iniciar com o ID do contrato ({contrato_id})"
        )


@router.post("/os-selo")
def importar_os_selo(
    arquivo: UploadFile = File(...),
    usuario=Depends(somente_admin_ou_master)
):
    """
    Importa arquivo de OS x Selo
    """
    _validar_nome_arquivo(arquivo.filename, usuario["contrato_id"])
    caminho = _salvar_arquivo_temporario(arquivo)
    
    return ImportService.importar_arquivo(
        caminho_excel=caminho,
        tipo_arquivo="os_selo",
        contrato_id=usuario["contrato_id"],
        email_usuario=usuario["email"],
        nome_arquivo=arquivo.filename
    )


@router.post("/os-lanc")
def importar_os_lanc(
    arquivo: UploadFile = File(...),
    usuario=Depends(somente_admin_ou_master)
):
    """
    Importa arquivo de OS x Lançamentos
    """
    _validar_nome_arquivo(arquivo.filename, usuario["contrato_id"])
    caminho = _salvar_arquivo_temporario(arquivo)
    
    return ImportService.importar_arquivo(
        caminho_excel=caminho,
        tipo_arquivo="os_lanc",
        contrato_id=usuario["contrato_id"],
        email_usuario=usuario["email"],
        nome_arquivo=arquivo.filename
    )


@router.post("/his-selo")
def importar_his_selo(
    arquivo: UploadFile = File(...),
    usuario=Depends(somente_admin_ou_master)
):
    """
    Importa arquivo de Histórico de Selos
    """
    _validar_nome_arquivo(arquivo.filename, usuario["contrato_id"])
    caminho = _salvar_arquivo_temporario(arquivo)
    
    return ImportService.importar_arquivo(
        caminho_excel=caminho,
        tipo_arquivo="his_selo",
        contrato_id=usuario["contrato_id"],
        email_usuario=usuario["email"],
        nome_arquivo=arquivo.filename
    )


@router.post("/his-selo-detalhe")
def importar_his_selo_detalhe(
    arquivo: UploadFile = File(...),
    usuario=Depends(somente_admin_ou_master)
):
    """
    Importa arquivo de Histórico de Selo Detalhe PR
    """
    _validar_nome_arquivo(arquivo.filename, usuario["contrato_id"])
    caminho = _salvar_arquivo_temporario(arquivo)
    
    return ImportService.importar_arquivo(
        caminho_excel=caminho,
        tipo_arquivo="his_selo_detalhe_pr",
        contrato_id=usuario["contrato_id"],
        email_usuario=usuario["email"],
        nome_arquivo=arquivo.filename
    )


@router.post("/tabela-lancamentos")
def importar_tabela_lancamentos(
    arquivo: UploadFile = File(...),
    usuario=Depends(somente_admin_ou_master)
):
    """
    Importa tabela de referência de lançamentos
    """
    _validar_nome_arquivo(arquivo.filename, usuario["contrato_id"])
    caminho = _salvar_arquivo_temporario(arquivo)
    
    return ImportService.importar_arquivo(
        caminho_excel=caminho,
        tipo_arquivo="tabela_de_lancamentos",
        contrato_id=usuario["contrato_id"],
        email_usuario=usuario["email"],
        nome_arquivo=arquivo.filename
    )
