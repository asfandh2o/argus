from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class EmployeeResponse(BaseModel):
    id: UUID
    name: str
    email: str
    role: str
    status: str
    latest_score: Optional[float] = None
    score_trend: Optional[str] = None  # "up", "down", "stable"

    class Config:
        from_attributes = True
