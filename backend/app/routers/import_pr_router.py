import os
import shutil
from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    Form,
    HTTPException
)

from app.core.permissions import somente_admin_ou_master
from app.core.import_config import ModoImportacao

# SERVICES
from app.services.import_tabela_lancamentos_pr_service import (
    importar_tabela_lancamentos_pr
)
from app.services.import_his_selo_detalhe_pr_service import (
    importar_his_selo_detalhe_pr
)
from app.services.import_os_selo_pr_service import (
    importar_os_selo_pr
)
from app.services.import_his_selo_pr_service import (
    importar_his_selo_pr
)
from app.services.import_os_lanc_pr_service import (
    importar_os_lanc_pr
)

router = APIRouter(
    prefix="/import/pr",
    tags=["Importação PR"]
)

# ======================================================
# FUNÇÕES AUXILIARES
# ======================================================

def _salvar_arquivo_temporario(arquivo: UploadFile) -> str:
    pasta_temp = "temp"
    os.makedirs(pasta_temp, exist_ok=True)

    caminho = os.path.join(pasta_temp, arquivo.filename)

    with open(caminho, "wb") as buffer:
        shutil.copyfileobj(arquivo.file, buffer)

    return caminho


def _validar_arquivo_basico(nome: str):
    if not nome.lower().endswith(".xlsx"):
        raise HTTPException(
            status_code=400,
            detail="Arquivo deve ser .xlsx"
        )

# ======================================================
# ENDPOINT — OS_SELO
# ======================================================

@router.post("/os-selo")
def importar_os_selo(
    arquivo: UploadFile = File(...),
    sistema_origem_id: int = Form(...),
    modo_importacao: ModoImportacao = Form(...),
    senha_confirmacao: str | None = Form(None),
    usuario=Depends(somente_admin_ou_master)
):
    _validar_arquivo_basico(arquivo.filename)
    caminho = _salvar_arquivo_temporario(arquivo)

    return importar_os_selo_pr(
        file=caminho,
        contrato_id=usuario["contrato_id"],
        usuario_email=usuario["email"],
        sistema_origem_id=sistema_origem_id,
        modo_importacao=modo_importacao,
        senha_confirmacao=senha_confirmacao
    )

# ======================================================
# ENDPOINT — OS_LANC (MIGRADO PARA SERVICE PRÓPRIO)
# ======================================================

@router.post("/os-lanc")
def importar_os_lanc(
    arquivo: UploadFile = File(...),
    sistema_origem_id: int = Form(...),
    modo_importacao: ModoImportacao = Form(...),
    senha_confirmacao: str | None = Form(None),
    usuario=Depends(somente_admin_ou_master)
):
    _validar_arquivo_basico(arquivo.filename)
    caminho = _salvar_arquivo_temporario(arquivo)

    return importar_os_lanc_pr(
        file=caminho,
        contrato_id=usuario["contrato_id"],
        usuario_email=usuario["email"],
        sistema_origem_id=sistema_origem_id,
        modo_importacao=modo_importacao,
        senha_confirmacao=senha_confirmacao
    )

# ======================================================
# ENDPOINT — HIS_SELO
# ======================================================

@router.post("/his-selo")
def importar_his_selo(
    arquivo: UploadFile = File(...),
    sistema_origem_id: int = Form(...),
    modo_importacao: ModoImportacao = Form(...),
    senha_confirmacao: str | None = Form(None),
    usuario=Depends(somente_admin_ou_master)
):
    _validar_arquivo_basico(arquivo.filename)
    caminho = _salvar_arquivo_temporario(arquivo)

    return importar_his_selo_pr(
        file=caminho,
        contrato_id=usuario["contrato_id"],
        usuario_email=usuario["email"],
        sistema_origem_id=sistema_origem_id,
        modo_importacao=modo_importacao,
        senha_confirmacao=senha_confirmacao
    )

# ======================================================
# ENDPOINT — TABELA DE LANÇAMENTOS (DIMENSÃO)
# ======================================================

@router.post("/tabela-lancamentos")
def importar_tabela_lancamentos(
    arquivo: UploadFile = File(...),
    usuario=Depends(somente_admin_ou_master)
):
    _validar_arquivo_basico(arquivo.filename)
    caminho = _salvar_arquivo_temporario(arquivo)

    return importar_tabela_lancamentos_pr(
        file=caminho,
        contrato_id=usuario["contrato_id"],
        usuario_email=usuario["email"]
    )

# ======================================================
# ENDPOINT — HIS_SELO_DETALHE
# ======================================================

@router.post("/his-selo-detalhe")
def importar_his_selo_detalhe(
    arquivo: UploadFile = File(...),
    sistema_origem_id: int = Form(...),
    modo_importacao: ModoImportacao = Form(...),
    senha_confirmacao: str | None = Form(None),
    usuario=Depends(somente_admin_ou_master)
):
    _validar_arquivo_basico(arquivo.filename)
    caminho = _salvar_arquivo_temporario(arquivo)

    return importar_his_selo_detalhe_pr(
        file=caminho,
        contrato_id=usuario["contrato_id"],
        usuario_email=usuario["email"],
        sistema_origem_id=sistema_origem_id,
        modo_importacao=modo_importacao,
        senha_confirmacao=senha_confirmacao
    )
