from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from db.session import get_db
from models.employee import Employee
from models.productivity_score import ProductivityScore
from api.deps import require_admin

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/team-stats")
async def team_stats(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_admin),
):
    """Aggregate team statistics for admin dashboard."""
    employees = (await db.execute(
        select(Employee).where(Employee.status == "active")
    )).scalars().all()

    scores_list = []
    for emp in employees:
        latest = (await db.execute(
            select(ProductivityScore)
            .where(ProductivityScore.employee_id == emp.id)
            .order_by(desc(ProductivityScore.score_date))
            .limit(1)
        )).scalar_one_or_none()

        if latest:
            scores_list.append(latest)

    if not scores_list:
        return {
            "team_average": 0,
            "highest_scorer": None,
            "lowest_scorer": None,
            "category_averages": {},
            "employee_count": len(employees),
            "scored_count": 0,
        }

    avg_overall = sum(s.overall_score for s in scores_list) / len(scores_list)
    avg_task = sum(s.task_score for s in scores_list) / len(scores_list)
    avg_time = sum(s.timeliness_score for s in scores_list) / len(scores_list)
    avg_comm = sum(s.communication_score for s in scores_list) / len(scores_list)
    avg_eng = sum(s.engagement_score for s in scores_list) / len(scores_list)

    best = max(scores_list, key=lambda s: s.overall_score)
    worst = min(scores_list, key=lambda s: s.overall_score)

    emp_map = {str(e.id): e.name for e in employees}

    return {
        "team_average": round(avg_overall, 1),
        "employee_count": len(employees),
        "scored_count": len(scores_list),
        "highest_scorer": {
            "name": emp_map.get(str(best.employee_id)),
            "score": best.overall_score,
        },
        "lowest_scorer": {
            "name": emp_map.get(str(worst.employee_id)),
            "score": worst.overall_score,
        },
        "category_averages": {
            "task": round(avg_task, 1),
            "timeliness": round(avg_time, 1),
            "communication": round(avg_comm, 1),
            "engagement": round(avg_eng, 1),
        },
    }
