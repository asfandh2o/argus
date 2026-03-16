from workers.celery_app import celery_app
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import select
from core.config import settings
from core.logging import get_logger
from datetime import date, datetime
import asyncio
import httpx
import uuid as uuid_mod

logger = get_logger(__name__)


def _create_session_factory():
    engine = create_async_engine(
        settings.DATABASE_URL, pool_size=5, max_overflow=5, pool_pre_ping=True,
    )
    return async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False,
        autocommit=False, autoflush=False,
    )


@celery_app.task(name="workers.tasks.sync_employees")
def sync_employees():
    asyncio.run(_sync_employees_async())


async def _sync_employees_async():
    """Pull employee list from HERA and upsert into local DB."""
    from models.employee import Employee

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(
                f"{settings.HERA_API_URL}/metrics/productivity",
                params={"api_key": settings.HERA_API_KEY, "days": 1},
            )
            if resp.status_code != 200:
                logger.error("hera_employee_sync_failed", status=resp.status_code)
                return
            data = resp.json()

        SessionLocal = _create_session_factory()
        async with SessionLocal() as db:
            synced = 0
            for m in data.get("metrics", []):
                result = await db.execute(
                    select(Employee).where(Employee.email == m["employee_email"])
                )
                existing = result.scalar_one_or_none()

                if existing:
                    existing.name = m["employee_name"]
                    existing.role = m.get("employee_role", existing.role)
                    existing.synced_at = datetime.utcnow()
                else:
                    emp = Employee(
                        id=uuid_mod.UUID(m["employee_id"]),
                        name=m["employee_name"],
                        email=m["employee_email"],
                        role=m.get("employee_role", "employee"),
                    )
                    db.add(emp)
                synced += 1

            await db.commit()
            logger.info("employees_synced", count=synced)

    except Exception as e:
        logger.error("employee_sync_error", error=str(e))


@celery_app.task(name="workers.tasks.collect_and_score")
def collect_and_score():
    asyncio.run(_collect_and_score_async())


async def _collect_and_score_async():
    """Collect metrics from HERA + ECHO, compute scores, generate advice."""
    from models.employee import Employee
    from models.metric_snapshot import MetricSnapshot
    from services.scoring_engine import ScoringEngine
    from services.advice_service import AdviceService

    SessionLocal = _create_session_factory()

    # Check we have employees
    async with SessionLocal() as db:
        employees = (await db.execute(select(Employee))).scalars().all()
        if not employees:
            logger.info("no_employees_to_score")
            return

    # Collect from HERA
    hera_data = {}
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(
                f"{settings.HERA_API_URL}/metrics/productivity",
                params={"api_key": settings.HERA_API_KEY, "days": 7},
            )
            if resp.status_code == 200:
                for m in resp.json().get("metrics", []):
                    hera_data[m["employee_email"]] = m
                logger.info("hera_metrics_collected", count=len(hera_data))
    except Exception as e:
        logger.error("hera_metrics_fetch_error", error=str(e))

    # Collect from ECHO
    echo_data = {}
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(
                f"{settings.ECHO_API_URL}/metrics/activity",
                params={"api_key": settings.ECHO_API_KEY, "days": 7},
            )
            if resp.status_code == 200:
                for m in resp.json().get("metrics", []):
                    echo_data[m["user_email"]] = m
                logger.info("echo_metrics_collected", count=len(echo_data))
    except Exception as e:
        logger.error("echo_metrics_fetch_error", error=str(e))

    # Score each employee
    scoring_engine = ScoringEngine()
    advice_service = AdviceService()
    today = date.today()

    async with SessionLocal() as db:
        scored = 0
        for emp in employees:
            hera_metrics = hera_data.get(emp.email, {})
            echo_metrics = echo_data.get(emp.email, {})

            # Save metric snapshots
            if hera_metrics:
                db.add(MetricSnapshot(
                    employee_id=emp.id, source="hera",
                    snapshot_date=today, data=hera_metrics,
                ))
            if echo_metrics:
                db.add(MetricSnapshot(
                    employee_id=emp.id, source="echo",
                    snapshot_date=today, data=echo_metrics,
                ))

            # Compute score
            score = scoring_engine.calculate(emp.id, hera_metrics, echo_metrics, today)
            db.add(score)
            await db.flush()

            # Generate AI advice
            try:
                advice_list = await advice_service.generate(emp, score, hera_metrics, echo_metrics)
                for a in advice_list:
                    db.add(a)
            except Exception as e:
                logger.error("advice_generation_failed", employee=emp.email, error=str(e))

            scored += 1

        await db.commit()
        logger.info("scoring_complete", employees_scored=scored, date=str(today))
