import os
import shutil
import traceback
from fastapi import APIRouter, UploadFile, File, Depends, Form

from app.core.permissions import somente_admin_ou_master
from app.core.import_config import ModoImportacao
from app.auth.dependencies import get_usuario_logado
from app.services.import_his_selo_detalhe_pr_service import (
    importar_his_selo_detalhe_pr
)

router = APIRouter(prefix="/import", tags=["Importações"])


@router.post(
    "/his-selo-detalhe-pr",
    dependencies=[Depends(somente_admin_ou_master)]
)
def importar_his_selo_detalhe_pr_endpoint(
    arquivo: UploadFile = File(...),
    modo_importacao: ModoImportacao = Form(...),
    senha_confirmacao: str | None = Form(None),
    usuario=Depends(get_usuario_logado),
):
    nome_arquivo = arquivo.filename

    # 1️⃣ Validar extensão
    if not nome_arquivo.lower().endswith(".xlsx"):
        raise ValueError("Arquivo deve ser .xlsx")

    # 2️⃣ Criar pasta temporária
    pasta_temp = "temp"
    os.makedirs(pasta_temp, exist_ok=True)

    caminho_arquivo = os.path.join(pasta_temp, nome_arquivo)

    # 3️⃣ Salvar arquivo
    with open(caminho_arquivo, "wb") as buffer:
        shutil.copyfileobj(arquivo.file, buffer)

    try:
        # 4️⃣ Chamar service REAL
        resultado = importar_his_selo_detalhe_pr(
            file=caminho_arquivo,
            contrato_id=usuario["contrato_id"],
            usuario_email=usuario["email"],
            usuario_id=usuario["id"],
            sistema_origem_id=usuario["sistema_origem_id"],
            modo_importacao=modo_importacao,
            senha_confirmacao=senha_confirmacao,
        )
        return resultado

    except Exception:
        # 🔥 EXPOR ERRO REAL EM DEV
        print("\n🔥 ERRO REAL NO ENDPOINT DE IMPORTAÇÃO 🔥")
        traceback.print_exc()
        print("🔥 FIM DO TRACEBACK 🔥\n")
        raise

    finally:
        # 5️⃣ Limpar arquivo temporário
        if os.path.exists(caminho_arquivo):
            os.remove(caminho_arquivo)
