from sqlalchemy.orm import Session
from app.models.metrics import Metric


def get_all_metrics(db: Session):
    return db.query(Metric).all()
