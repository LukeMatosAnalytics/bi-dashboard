from fastapi import FastAPI
from app.routers import health

app = FastAPI(title="BI Dashboard API")

app.include_router(health.router)
