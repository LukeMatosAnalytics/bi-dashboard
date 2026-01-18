from pydantic import BaseModel
from typing import Optional


class ErrorDocumentation(BaseModel):
    error_code: str
    message: str
    http_status: int
    action: Optional[str]


class ErrorDocumentationResponse(BaseModel):
    success: bool
    data: list[ErrorDocumentation]
