from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class AdviceResponse(BaseModel):
    id: UUID
    employee_id: UUID
    content: str
    category: str
    priority: str
    dismissed: bool
    context: dict
    created_at: datetime

    class Config:
        from_attributes = True
