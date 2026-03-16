from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List
from db.session import get_db
from models.employee import Employee
from models.productivity_score import ProductivityScore
from schemas.employee import EmployeeResponse
from api.deps import require_admin

router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("/", response_model=List[EmployeeResponse])
async def list_employees(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_admin),
):
    """List all employees with their latest scores."""
    employees = (await db.execute(
        select(Employee).order_by(Employee.name)
    )).scalars().all()

    results = []
    for emp in employees:
        scores = (await db.execute(
            select(ProductivityScore)
            .where(ProductivityScore.employee_id == emp.id)
            .order_by(desc(ProductivityScore.score_date))
            .limit(2)
        )).scalars().all()

        latest_score = scores[0].overall_score if scores else None
        trend = None
        if len(scores) >= 2:
            diff = scores[0].overall_score - scores[1].overall_score
            trend = "up" if diff > 2 else ("down" if diff < -2 else "stable")

        results.append(EmployeeResponse(
            id=emp.id,
            name=emp.name,
            email=emp.email,
            role=emp.role,
            status=emp.status,
            latest_score=latest_score,
            score_trend=trend,
        ))

    return results
