from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from app.core.config import settings

from app.routers import metrics
from app.routers.auth_router import router as auth_router
from app.routers.import_pr_router import router as import_pr_router
from app.routers.import_query_router import router as import_query_router
from app.routers.bi_preview import router as bi_preview_router

app = FastAPI(title=settings.APP_NAME)

# 🔐 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ LIBERAR PREFLIGHT (OPTIONS) GLOBALMENTE
@app.options("/{path:path}")
async def preflight_handler(path: str, request: Request):
    return Response(status_code=200)

# 📊 Routers
app.include_router(metrics.router)
app.include_router(auth_router)
app.include_router(import_pr_router)
app.include_router(import_query_router)
app.include_router(bi_preview_router)
