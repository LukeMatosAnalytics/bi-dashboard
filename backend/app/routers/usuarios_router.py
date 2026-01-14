"""
Endpoints de gerenciamento de usuários
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlalchemy import text

from app.core.database import engine
from app.core.permissions import somente_master, somente_admin_ou_master
from app.core.security import gerar_hash_senha

router = APIRouter(prefix="/usuarios", tags=["Usuários"])


class UsuarioCreate(BaseModel):
    email: EmailStr
    senha: str
    nome: str
    role: str
    contrato_id: str


class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    role: Optional[str] = None
    ativo: Optional[bool] = None


@router.get("/")
def listar_usuarios(usuario=Depends(somente_admin_ou_master)):
    """
    Lista usuários. MASTER vê todos, ADMIN vê apenas do seu contrato.
    """
    if usuario["role"] == "MASTER":
        sql = """
        SELECT u.usuario_id, u.email, u.nome, u.role, u.contrato_id, 
               u.ativo, u.created_at, c.nome as contrato_nome
        FROM control.usuarios u
        LEFT JOIN control.contratos c ON u.contrato_id = c.contrato_id
        ORDER BY u.created_at DESC
        """
        params = {}
    else:
        sql = """
        SELECT u.usuario_id, u.email, u.nome, u.role, u.contrato_id, 
               u.ativo, u.created_at, c.nome as contrato_nome
        FROM control.usuarios u
        LEFT JOIN control.contratos c ON u.contrato_id = c.contrato_id
        WHERE u.contrato_id = :contrato_id
        ORDER BY u.created_at DESC
        """
        params = {"contrato_id": usuario["contrato_id"]}
    
    with engine.connect() as conn:
        result = conn.execute(text(sql), params).mappings().all()
    
    return [dict(r) for r in result]


@router.post("/")
def criar_usuario(dados: UsuarioCreate, usuario=Depends(somente_master)):
    """
    Cria novo usuário (apenas MASTER)
    """
    # Verifica se email já existe
    with engine.connect() as conn:
        existe = conn.execute(
            text("SELECT 1 FROM control.usuarios WHERE email = :email"),
            {"email": dados.email}
        ).first()
        
        if existe:
            raise HTTPException(400, "Email já cadastrado")
    
    # Gera hash da senha
    senha_hash = gerar_hash_senha(dados.senha)
    
    sql = """
    INSERT INTO control.usuarios (email, senha_hash, nome, role, contrato_id, ativo, status)
    VALUES (:email, :senha_hash, :nome, :role, :contrato_id, true, 'ATIVO')
    RETURNING usuario_id
    """
    
    with engine.begin() as conn:
        result = conn.execute(text(sql), {
            "email": dados.email,
            "senha_hash": senha_hash,
            "nome": dados.nome,
            "role": dados.role,
            "contrato_id": dados.contrato_id
        })
        usuario_id = result.fetchone()[0]
    
    return {"message": "Usuário criado", "usuario_id": usuario_id}


@router.put("/{usuario_id}")
def atualizar_usuario(
    usuario_id: int,
    dados: UsuarioUpdate,
    usuario=Depends(somente_master)
):
    """
    Atualiza usuário (apenas MASTER)
    """
    updates = []
    params = {"usuario_id": usuario_id}
    
    if dados.nome is not None:
        updates.append("nome = :nome")
        params["nome"] = dados.nome
    
    if dados.role is not None:
        updates.append("role = :role")
        params["role"] = dados.role
    
    if dados.ativo is not None:
        updates.append("ativo = :ativo")
        params["ativo"] = dados.ativo
    
    if not updates:
        raise HTTPException(400, "Nenhum campo para atualizar")
    
    sql = f"""
    UPDATE control.usuarios 
    SET {', '.join(updates)}, updated_at = CURRENT_TIMESTAMP
    WHERE usuario_id = :usuario_id
    """
    
    with engine.begin() as conn:
        conn.execute(text(sql), params)
    
    return {"message": "Usuário atualizado"}
