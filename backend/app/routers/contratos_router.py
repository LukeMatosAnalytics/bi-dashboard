"""
Endpoints de gerenciamento de contratos
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import text

from app.core.database import engine
from app.core.permissions import somente_master
from app.core.auth import get_usuario_atual

router = APIRouter(prefix="/contratos", tags=["Contratos"])


class ContratoCreate(BaseModel):
    contrato_id: str
    nome: str
    nome_fantasia: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None
    vertical: Optional[str] = None


@router.get("/")
def listar_contratos(usuario=Depends(get_usuario_atual)):
    """
    Lista contratos. MASTER vê todos, outros vêem apenas o seu.
    """
    if usuario["role"] == "MASTER":
        sql = """
        SELECT contrato_id, nome, nome_fantasia, cidade, uf, vertical, status, created_at
        FROM control.contratos
        ORDER BY nome
        """
        params = {}
    else:
        sql = """
        SELECT contrato_id, nome, nome_fantasia, cidade, uf, vertical, status, created_at
        FROM control.contratos
        WHERE contrato_id = :contrato_id
        """
        params = {"contrato_id": usuario["contrato_id"]}
    
    with engine.connect() as conn:
        result = conn.execute(text(sql), params).mappings().all()
    
    return [dict(r) for r in result]


@router.post("/")
def criar_contrato(dados: ContratoCreate, usuario=Depends(somente_master)):
    """
    Cria novo contrato (apenas MASTER)
    """
    sql = """
    INSERT INTO control.contratos (contrato_id, nome, nome_fantasia, cidade, uf, vertical, status)
    VALUES (:contrato_id, :nome, :nome_fantasia, :cidade, :uf, :vertical, 'ATIVO')
    ON CONFLICT (contrato_id) DO NOTHING
    RETURNING contrato_id
    """
    
    with engine.begin() as conn:
        result = conn.execute(text(sql), dados.model_dump())
        row = result.fetchone()
        
        if not row:
            raise HTTPException(400, "Contrato já existe")
    
    return {"message": "Contrato criado", "contrato_id": dados.contrato_id}
