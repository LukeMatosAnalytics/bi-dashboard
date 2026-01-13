from pydantic import BaseModel
from typing import Optional


class LoginRequest(BaseModel):
    email: str
    senha: str


class LoginResponse(BaseModel):
    sucesso: bool
    email: Optional[str] = None
    role: Optional[str] = None
    contrato_id: Optional[str] = None
    erro: Optional[str] = None
