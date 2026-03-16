import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from db.session import Base


class Advice(Base):
    __tablename__ = "advice"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True)
    score_id = Column(UUID(as_uuid=True), ForeignKey("productivity_scores.id", ondelete="SET NULL"), nullable=True)
    content = Column(Text, nullable=False)
    category = Column(String, nullable=False)  # focus, time_management, communication, engagement
    priority = Column(String, default="medium")  # high, medium, low
    dismissed = Column(Boolean, default=False)
    context = Column(JSONB, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
