from app.core.database import engine

def test_connection():
    with engine.connect() as connection:
        return "Connection OK"
