from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


# ======================================================
# ITEM — LOG DE IMPORTAÇÃO
# ======================================================

class ImportLogItemSchema(BaseModel):
    id: int
    contrato_id: str
    sistema_origem_id: Optional[int]

    usuario_id: int
    usuario_email: str

    tipo_arquivo: str
    nome_arquivo: str
    modo_importacao: str

    status: str
    error_code: Optional[str]
    mensagem: Optional[str]

    total_registros: int
    registros_processados: int

    started_at: datetime
    finished_at: Optional[datetime]

    class Config:
        from_attributes = True


# ======================================================
# META — PAGINAÇÃO / AUDITORIA
# ======================================================

class ImportLogListMetaSchema(BaseModel):
    total: int
    limit: int
    offset: int


# ======================================================
# RESPONSE — LISTA DE LOGS
# ======================================================

class ImportLogListResponseSchema(BaseModel):
    success: bool
    data: List[ImportLogItemSchema]
    meta: ImportLogListMetaSchema
