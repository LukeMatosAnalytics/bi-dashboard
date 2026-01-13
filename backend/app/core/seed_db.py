from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from backend.app.models.metrics import Metric


def seed_metrics():
    db: Session = SessionLocal()

    try:
        # Evita duplicar seed
        if db.query(Metric).first():
            print("Seed já executado. Nenhuma ação necessária.")
            return

        now = datetime.utcnow()

        metrics = [
            Metric(name="Atendimentos", value=120, category="Operacional", created_at=now - timedelta(days=3)),
            Metric(name="Atendimentos", value=98, category="Operacional", created_at=now - timedelta(days=2)),
            Metric(name="Atendimentos", value=143, category="Operacional", created_at=now - timedelta(days=1)),

            Metric(name="Satisfação", value=4.5, category="Qualidade", created_at=now - timedelta(days=3)),
            Metric(name="Satisfação", value=4.2, category="Qualidade", created_at=now - timedelta(days=2)),
            Metric(name="Satisfação", value=4.7, category="Qualidade", created_at=now - timedelta(days=1)),

            Metric(name="Receita", value=25000, category="Financeiro", created_at=now - timedelta(days=3)),
            Metric(name="Receita", value=27000, category="Financeiro", created_at=now - timedelta(days=2)),
            Metric(name="Receita", value=30000, category="Financeiro", created_at=now - timedelta(days=1)),
        ]

        db.add_all(metrics)
        db.commit()

        print("Seed executado com sucesso!")

    finally:
        db.close()
