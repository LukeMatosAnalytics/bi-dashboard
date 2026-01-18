from typing import Any, Optional


def success_response(
    *,
    code: str,
    message: str,
    data: Optional[Any] = None
):
    return {
        "success": True,
        "code": code,
        "message": message,
        "data": data
    }


def error_response(
    *,
    code: str,
    message: str,
    details: Optional[Any] = None,
    support_hint: Optional[str] = None
):
    return {
        "success": False,
        "code": code,
        "message": message,
        "details": details,
        "support_hint": support_hint
    }
