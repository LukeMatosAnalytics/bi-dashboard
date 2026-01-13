from datetime import datetime
from pydantic import BaseModel


class MetricResponse(BaseModel):
    id: int
    name: str
    value: float
    category: str | None
    created_at: datetime

    class Config:
        from_attributes = True
