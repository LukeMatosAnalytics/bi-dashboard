from typing import Any, Dict, Optional


def success_response(
    *,
    data: Optional[Dict[str, Any]] = None,
    meta: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Resposta padrão de sucesso da API.

    - data: resultado funcional da operação
    - meta: informações operacionais (logs, auditoria, suporte)
    """
    return {
        "success": True,
        "data": data or {},
        "meta": meta or {}
    }


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
    Normalmente usada apenas em handlers globais.
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
