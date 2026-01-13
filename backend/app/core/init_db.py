from app.core.database import engine
from app.models.base import Base

# Importa os models para registrar no metadata
from app.models import metrics  # noqa

def init_db():
    Base.metadata.create_all(bind=engine)
