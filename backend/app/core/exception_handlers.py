from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.core.errors import ErrorCode, ERROR_CATALOG
from app.core.exceptions import AppException, BusinessException


# ======================================================
# HANDLER — ERROS DE NEGÓCIO
# ======================================================

def business_exception_handler(
    request: Request,
    exc: BusinessException
):
    """
    Handler para exceções de negócio controladas.
    """

    payload = {
        "success": False,
        "error": {
            "code": exc.error_code,
            "message": exc.message,
        }
    }

    if exc.detail:
        payload["error"]["detail"] = exc.detail

    if exc.extra:
        payload["error"]["extra"] = exc.extra

    if exc.action:
        payload["error"]["action"] = exc.action

    return JSONResponse(
        status_code=exc.http_status,
        content=payload
    )


# ======================================================
# HANDLER — ERROS DE BANCO DE DADOS
# ======================================================

def sqlalchemy_exception_handler(
    request: Request,
    exc: SQLAlchemyError
):
    error_info = ERROR_CATALOG[ErrorCode.DATABASE_ERROR]

    return JSONResponse(
        status_code=error_info["http_status"],
        content={
            "success": False,
            "error": {
                "code": ErrorCode.DATABASE_ERROR,
                "message": error_info["message"],
                "action": error_info.get("action"),
            }
        }
    )


# ======================================================
# HANDLER — ERRO GENÉRICO
# ======================================================

def generic_exception_handler(
    request: Request,
    exc: Exception
):
    error_info = ERROR_CATALOG[ErrorCode.UNEXPECTED_ERROR]

    return JSONResponse(
        status_code=error_info["http_status"],
        content={
            "success": False,
            "error": {
                "code": ErrorCode.UNEXPECTED_ERROR,
                "message": error_info["message"],
                "action": error_info.get("action"),
            }
        }
    )
