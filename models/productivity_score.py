import uuid
from datetime import datetime
from sqlalchemy import Column, Float, DateTime, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from db.session import Base


class ProductivityScore(Base):
    __tablename__ = "productivity_scores"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True)
    score_date = Column(Date, nullable=False, index=True)

    overall_score = Column(Float, nullable=False)
    task_score = Column(Float, nullable=False)
    timeliness_score = Column(Float, nullable=False)
    communication_score = Column(Float, nullable=False)
    engagement_score = Column(Float, nullable=False)

    weights = Column(JSONB, nullable=False, default={
        "task": 0.40, "timeliness": 0.25,
        "communication": 0.20, "engagement": 0.15
    })

    raw_metrics = Column(JSONB, nullable=False, default={})

    created_at = Column(DateTime, default=datetime.utcnow)
