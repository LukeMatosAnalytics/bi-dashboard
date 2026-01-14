"""
BI Dashboard API - Ponto de entrada principal
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import (
    auth_router,
    import_pr_router,
    import_query_router,
    dashboard_router,
    health_router,
    usuarios_router,
    contratos_router
)

# Cria aplicação
app = FastAPI(
    title=settings.APP_NAME,
    description="API para plataforma de BI multi-cliente",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(",") if settings.CORS_ORIGINS else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra routers
app.include_router(health_router.router)
app.include_router(auth_router.router)
app.include_router(dashboard_router.router)
app.include_router(import_pr_router.router)
app.include_router(import_query_router.router)
app.include_router(usuarios_router.router)
app.include_router(contratos_router.router)


@app.get("/")
def root():
    return {
        "app": settings.APP_NAME,
        "status": "online",
        "docs": "/docs"
    }
