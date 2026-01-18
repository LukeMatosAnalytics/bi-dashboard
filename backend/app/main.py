from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from sqlalchemy.exc import SQLAlchemyError
import traceback

from app.core.config import settings
from app.core.exceptions import BusinessException
from app.core.exception_handlers import (
    business_exception_handler,
    sqlalchemy_exception_handler,
    generic_exception_handler,
)

from app.routers import metrics
from app.routers.auth_router import router as auth_router

# 🔹 IMPORT ROUTERS
from app.routers.import_router import router as import_router
from app.routers.import_pr_router import router as import_pr_router
from app.routers.import_query_router import router as import_query_router
from app.routers.import_logs_router import router as import_logs_router

# 🔹 BI / SISTEMA
from app.routers.bi_preview import router as bi_preview_router
from app.routers.bi_router import router as bi_router
from app.routers.errors_router import router as errors_router
from app.routers.system_router import router as system_router


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)

# ======================================================
# CORS
# ======================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================================================
# PREFLIGHT (OPTIONS)
# ======================================================

@app.options("/{path:path}")
async def preflight_handler(path: str, request: Request):
    return Response(status_code=200)

# ======================================================
# HANDLERS GLOBAIS DE EXCEÇÃO
# ======================================================

app.add_exception_handler(
    BusinessException,
    business_exception_handler
)

app.add_exception_handler(
    SQLAlchemyError,
    sqlalchemy_exception_handler
)

# 🔥 AJUSTE TEMPORÁRIO PARA DEV
@app.exception_handler(Exception)
async def debug_generic_exception_handler(request, exc):
    return generic_exception_handler(request, exc)


# ======================================================
# ROTAS
# ======================================================

app.include_router(metrics.router)
app.include_router(auth_router)

# 🔹 IMPORTAÇÕES
app.include_router(import_router)        # upload do Excel
app.include_router(import_pr_router)
app.include_router(import_query_router)
app.include_router(import_logs_router)

# 🔹 BI / SISTEMA
app.include_router(bi_preview_router)
app.include_router(bi_router)
app.include_router(errors_router)
app.include_router(system_router)
