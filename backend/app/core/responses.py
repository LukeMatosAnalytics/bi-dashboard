from typing import Any, Dict, Optional

from app.core.success_codes import SuccessCode
from app.core.success_catalog import SUCCESS_CATALOG


# ======================================================
# RESPOSTA DE SUCESSO PADRONIZADA
# ======================================================

def success_response(
    *,
    code: SuccessCode,
    data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Resposta padrão de sucesso da API.

    - code: código semântico de sucesso (SuccessCode)
    - data: resultado funcional da operação
    """

    if code not in SUCCESS_CATALOG:
        raise RuntimeError(
            f"SuccessCode {code} não registrado no SUCCESS_CATALOG"
        )

    catalog = SUCCESS_CATALOG[code]

    return {
        "success": True,
        "data": data or {},
        "meta": {
            "code": code,
            "message": catalog["message"]
        }
    }


# ======================================================
# RESPOSTA DE ERRO PADRONIZADA
# (usada principalmente pelos handlers globais)
# ======================================================

def error_response(
    *,
    code: str,
    message: str,
    detail: Optional[str] = None,
    action: Optional[str] = None,
    extra: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Resposta de erro padronizada.

    - code: código de erro (ErrorCode)
    - message: mensagem principal
    - detail: detalhe técnico ou contextual
    - action: orientação para suporte N2/N3
    - extra: payload técnico adicional
    """

    payload = {
        "success": False,
        "error": {
            "code": code,
            "message": message
        }
    }

    if detail:
        payload["error"]["detail"] = detail

    if action:
        payload["error"]["action"] = action

    if extra:
        payload["error"]["extra"] = extra

    return payload
