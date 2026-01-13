import os
import shutil
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException

from app.core.permissions import somente_admin_ou_master
from app.services.import_service import importar_em_chunks

router = APIRouter(
    prefix="/import/pr",
    tags=["Importação PR"]
)


# ==============================
# FUNÇÃO AUXILIAR
# ==============================

def _salvar_arquivo_temporario(arquivo: UploadFile) -> str:
    pasta_temp = "temp"
    os.makedirs(pasta_temp, exist_ok=True)

    caminho = os.path.join(pasta_temp, arquivo.filename)

    with open(caminho, "wb") as buffer:
        shutil.copyfileobj(arquivo.file, buffer)

    return caminho


def _validar_nome_arquivo(nome: str, contrato_id: str):
    if not nome.lower().endswith(".xlsx"):
        raise HTTPException(400, "Arquivo deve ser .xlsx")

    if not nome.startswith(contrato_id):
        raise HTTPException(
            403,
            "Arquivo não pertence ao contrato do usuário"
        )


# ==============================
# ENDPOINTS
# ==============================

@router.post("/os-selo")
def importar_os_selo(
    arquivo: UploadFile = File(...),
    usuario=Depends(somente_admin_ou_master)
):
    _validar_nome_arquivo(arquivo.filename, usuario["contrato_id"])
    caminho = _salvar_arquivo_temporario(arquivo)

    return importar_em_chunks(
        caminho_excel=caminho,
        tabela="os_selo",
        contrato_id=usuario["contrato_id"],
        email_usuario=usuario["email"],
        nome_arquivo=arquivo.filename,
        tipo_arquivo="os_selo"
    )


@router.post("/os-lanc")
def importar_os_lanc(
    arquivo: UploadFile = File(...),
    usuario=Depends(somente_admin_ou_master)
):
    _validar_nome_arquivo(arquivo.filename, usuario["contrato_id"])
    caminho = _salvar_arquivo_temporario(arquivo)

    return importar_em_chunks(
        caminho_excel=caminho,
        tabela="os_lanc",
        contrato_id=usuario["contrato_id"],
        email_usuario=usuario["email"],
        nome_arquivo=arquivo.filename,
        tipo_arquivo="os_lanc"
    )


@router.post("/his-selo")
def importar_his_selo(
    arquivo: UploadFile = File(...),
    usuario=Depends(somente_admin_ou_master)
):
    _validar_nome_arquivo(arquivo.filename, usuario["contrato_id"])
    caminho = _salvar_arquivo_temporario(arquivo)

    return importar_em_chunks(
        caminho_excel=caminho,
        tabela="his_selo",
        contrato_id=usuario["contrato_id"],
        email_usuario=usuario["email"],
        nome_arquivo=arquivo.filename,
        tipo_arquivo="his_selo"
    )


@router.post("/tabela-lancamentos")
def importar_tabela_lancamentos(
    arquivo: UploadFile = File(...),
    usuario=Depends(somente_admin_ou_master)
):
    _validar_nome_arquivo(arquivo.filename, usuario["contrato_id"])
    caminho = _salvar_arquivo_temporario(arquivo)

    return importar_em_chunks(
        caminho_excel=caminho,
        tabela="tabela_de_lancamentos",
        contrato_id=usuario["contrato_id"],
        email_usuario=usuario["email"],
        nome_arquivo=arquivo.filename,
        tipo_arquivo="tabela_de_lancamentos"
    )
