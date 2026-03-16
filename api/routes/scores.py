from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List
from uuid import UUID
from db.session import get_db
from models.employee import Employee
from models.productivity_score import ProductivityScore
from schemas.score import ScoreResponse, ScoreSummary
from api.deps import get_current_user, require_admin

router = APIRouter(prefix="/scores", tags=["scores"])


@router.get("/me", response_model=List[ScoreResponse])
async def my_scores(
    limit: int = 30,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get score history for the current employee."""
    if current_user["role"] == "admin":
        raise HTTPException(status_code=400, detail="Admin has no scores. Use /scores/{employee_id}")

    scores = (await db.execute(
        select(ProductivityScore)
        .where(ProductivityScore.employee_id == current_user["id"])
        .order_by(desc(ProductivityScore.score_date))
        .limit(limit)
    )).scalars().all()

    return [ScoreResponse.model_validate(s) for s in scores]


@router.get("/team/summary", response_model=List[ScoreSummary])
async def team_summary(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_admin),
):
    """Get latest score summary for all employees (admin dashboard)."""
    employees = (await db.execute(
        select(Employee).where(Employee.status == "active").order_by(Employee.name)
    )).scalars().all()

    summaries = []
    for emp in employees:
        scores = (await db.execute(
            select(ProductivityScore)
            .where(ProductivityScore.employee_id == emp.id)
            .order_by(desc(ProductivityScore.score_date))
            .limit(2)
        )).scalars().all()

        if not scores:
            continue

        current = scores[0]
        previous = scores[1] if len(scores) >= 2 else None
        diff = (current.overall_score - previous.overall_score) if previous else 0
        trend = "up" if diff > 2 else ("down" if diff < -2 else "stable")

        summaries.append(ScoreSummary(
            employee_id=emp.id,
            employee_name=emp.name,
            employee_email=emp.email,
            employee_role=emp.role,
            current_score=current.overall_score,
            previous_score=previous.overall_score if previous else None,
            trend=trend,
            task_score=current.task_score,
            timeliness_score=current.timeliness_score,
            communication_score=current.communication_score,
            engagement_score=current.engagement_score,
        ))

    return summaries


@router.get("/{employee_id}", response_model=List[ScoreResponse])
async def employee_scores(
    employee_id: UUID,
    limit: int = 30,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_admin),
):
    """Get score history for a specific employee (admin only)."""
    scores = (await db.execute(
        select(ProductivityScore)
        .where(ProductivityScore.employee_id == employee_id)
        .order_by(desc(ProductivityScore.score_date))
        .limit(limit)
    )).scalars().all()

    return [ScoreResponse.model_validate(s) for s in scores]
