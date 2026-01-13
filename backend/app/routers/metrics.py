from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.repositories.metrics_repository import get_all_metrics
from app.schemas.metrics import MetricResponse

router = APIRouter(prefix="/metrics", tags=["Metrics"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[MetricResponse])
def list_metrics(db: Session = Depends(get_db)):
    return get_all_metrics(db)
