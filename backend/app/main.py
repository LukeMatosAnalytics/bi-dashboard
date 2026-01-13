from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import metrics
from app.routers.auth_router import router as auth_router
from app.routers.import_pr_router import router as import_pr_router
from app.routers.import_query_router import router as import_query_router

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(metrics.router)
app.include_router(auth_router)
app.include_router(import_pr_router)
app.include_router(import_query_router)
