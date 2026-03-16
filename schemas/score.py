from pydantic import BaseModel
from uuid import UUID
from datetime import date, datetime
from typing import Optional


class ScoreResponse(BaseModel):
    id: UUID
    employee_id: UUID
    score_date: date
    overall_score: float
    task_score: float
    timeliness_score: float
    communication_score: float
    engagement_score: float
    weights: dict
    raw_metrics: dict
    created_at: datetime

    class Config:
        from_attributes = True


class ScoreSummary(BaseModel):
    employee_id: UUID
    employee_name: str
    employee_email: str
    employee_role: str
    current_score: float
    previous_score: Optional[float] = None
    trend: str  # "up", "down", "stable"
    task_score: float
    timeliness_score: float
    communication_score: float
    engagement_score: float
