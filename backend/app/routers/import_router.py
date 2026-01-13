import os
import shutil
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException

from app.core.permissions import somente_admin_ou_master
from app.services.import_service import importar_his_selo_detalhe_pr

router = APIRouter(prefix="/import", tags=["Importação"])


@router.post("/his-selo-detalhe-pr")
def importar_his_selo_detalhe_pr_endpoint(
    arquivo: UploadFile = File(...),
    usuario=Depends(somente_admin_ou_master)
):
    nome_arquivo = arquivo.filename

    # 1️⃣ Validar extensão
    if not nome_arquivo.lower().endswith(".xlsx"):
        raise HTTPException(
            status_code=400,
            detail="Arquivo deve ser .xlsx"
        )

    # 2️⃣ Validar padrão do nome
    partes = nome_arquivo.split("_", 1)
    if len(partes) != 2:
        raise HTTPException(
            status_code=400,
            detail="Nome do arquivo fora do padrão <CONTRATO>_arquivo.xlsx"
        )

    contrato_arquivo, nome_logico = partes

    # 3️⃣ Validar contrato
    if usuario["role"] != "MASTER":
        if contrato_arquivo != usuario["contrato_id"]:
            raise HTTPException(
                status_code=403,
                detail="Arquivo não pertence ao contrato do usuário"
            )

    # 4️⃣ Validar tipo de arquivo
    if not nome_logico.startswith("export_his_selo_detalhe_pr"):
        raise HTTPException(
            status_code=400,
            detail="Arquivo incorreto para este endpoint"
        )

    # 5️⃣ Salvar arquivo temporário
    pasta_temp = "temp"
    os.makedirs(pasta_temp, exist_ok=True)

    caminho_arquivo = os.path.join(pasta_temp, nome_arquivo)

    with open(caminho_arquivo, "wb") as buffer:
        shutil.copyfileobj(arquivo.file, buffer)

    # 6️⃣ Importar (AGORA com TODOS os parâmetros)
    resultado = importar_his_selo_detalhe_pr(
        caminho_arquivo=caminho_arquivo,
        contrato_id=contrato_arquivo,
        email_usuario=usuario["email"],
        nome_arquivo=nome_arquivo
    )

    os.remove(caminho_arquivo)

    return resultado
