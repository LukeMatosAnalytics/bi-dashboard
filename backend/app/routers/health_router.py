"""
Endpoints de saúde da aplicação
"""
from fastapi import APIRouter
from sqlalchemy import text
from app.core.database import engine

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/")
def health_check():
    """Verifica se a API está online"""
    return {"status": "healthy"}


@router.get("/db")
def database_check():
    """Verifica conexão com o banco"""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"database": "connected"}
    except Exception as e:
        return {"database": "error", "detail": str(e)}
