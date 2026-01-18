from typing import Any, Dict, Optional
from fastapi import HTTPException

from app.core.errors import ErrorCode, ERROR_CATALOG


class AppException(Exception):
    """
    Exceção base da aplicação.

    Todas as exceções controladas do sistema
    devem herdar desta classe.
    """

    error_code: ErrorCode
    message: str
    detail: Optional[str]
    extra: Dict[str, Any]

    def __init__(
        self,
        *,
        error_code: ErrorCode,
        message: str,
        detail: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None,
    ):
        self.error_code = error_code
        self.message = message
        self.detail = detail
        self.extra = extra or {}

        super().__init__(message)


class BusinessException(AppException):
    """
    Exceção de negócio padronizada.

    Sempre baseada em um ErrorCode definido no ERROR_CATALOG.
    """

    http_status: int
    action: Optional[str]

    def __init__(
        self,
        error_code: ErrorCode,
        *,
        detail: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None,
    ):
        if error_code not in ERROR_CATALOG:
            raise RuntimeError(
                f"ErrorCode {error_code} não está registrado no ERROR_CATALOG"
            )

        catalog = ERROR_CATALOG[error_code]

        self.http_status = catalog["http_status"]
        self.action = catalog.get("action")

        super().__init__(
            error_code=error_code,
            message=catalog["message"],
            detail=detail,
            extra=extra,
        )

    def to_http_exception(self) -> HTTPException:
        """
        Converte a exceção de negócio em HTTPException
        para resposta padronizada da API.
        """
        payload = {
            "error_code": self.error_code,
            "message": self.message,
        }

        if self.detail:
            payload["detail"] = self.detail

        if self.extra:
            payload["extra"] = self.extra

        if self.action:
            payload["action"] = self.action

        return HTTPException(
            status_code=self.http_status,
            detail=payload
        )
