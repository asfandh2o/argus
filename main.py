from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from core.logging import configure_logging, get_logger
from api.routes import auth, employees, scores, advice, dashboard
from db.session import engine, Base

configure_logging()
logger = get_logger(__name__)

app = FastAPI(
    title="ARGUS - Productivity Intelligence",
    description="NORA's transparent productivity scoring and AI advice engine.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(employees.router)
app.include_router(scores.router)
app.include_router(advice.router)
app.include_router(dashboard.router)


@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("argus_started", environment=settings.ENVIRONMENT)


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("argus_shutting_down")
    await engine.dispose()


@app.get("/")
async def root():
    return {"service": "ARGUS", "version": "1.0.0", "status": "operational"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)
