from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.get("/db-check")
def db_check():
    from app.repositories.test_repository import test_connection
    return {"database": test_connection()}
