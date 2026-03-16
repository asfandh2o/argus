import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from db.session import Base


class MetricSnapshot(Base):
    __tablename__ = "metric_snapshots"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True)
    source = Column(String, nullable=False)  # "hera" or "echo"
    snapshot_date = Column(Date, nullable=False, index=True)
    data = Column(JSONB, nullable=False)
    collected_at = Column(DateTime, default=datetime.utcnow)
