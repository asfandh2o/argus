from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List
from uuid import UUID
from db.session import get_db
from models.advice import Advice
from schemas.advice import AdviceResponse
from api.deps import get_current_user, require_admin

router = APIRouter(prefix="/advice", tags=["advice"])


@router.get("/me", response_model=List[AdviceResponse])
async def my_advice(
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get latest advice for the current employee."""
    if current_user["role"] == "admin":
        raise HTTPException(status_code=400, detail="Use /advice/{employee_id}")

    advice = (await db.execute(
        select(Advice)
        .where(Advice.employee_id == current_user["id"], Advice.dismissed == False)
        .order_by(desc(Advice.created_at))
        .limit(limit)
    )).scalars().all()

    return [AdviceResponse.model_validate(a) for a in advice]


@router.get("/{employee_id}", response_model=List[AdviceResponse])
async def employee_advice(
    employee_id: UUID,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_admin),
):
    """Get advice for a specific employee (admin only)."""
    advice = (await db.execute(
        select(Advice)
        .where(Advice.employee_id == employee_id)
        .order_by(desc(Advice.created_at))
        .limit(limit)
    )).scalars().all()

    return [AdviceResponse.model_validate(a) for a in advice]


@router.patch("/{advice_id}/dismiss")
async def dismiss_advice(
    advice_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Dismiss an advice item."""
    result = await db.execute(select(Advice).where(Advice.id == advice_id))
    advice = result.scalar_one_or_none()
    if not advice:
        raise HTTPException(status_code=404, detail="Advice not found")

    if current_user["role"] == "employee" and str(advice.employee_id) != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not your advice")

    advice.dismissed = True
    await db.commit()
    return {"status": "dismissed"}
