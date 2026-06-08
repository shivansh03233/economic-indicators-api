from sqlalchemy import Column, Integer, String, Float, DateTime, Index
from sqlalchemy.sql import func
from app.database import Base


class IndicatorRecord(Base):
    __tablename__ = "indicator_records"

    id = Column(Integer, primary_key=True, index=True)
    indicator = Column(String, nullable=False)   # e.g. "cpi", "fed_rate"
    country = Column(String, nullable=False, default="US")
    value = Column(Float, nullable=False)
    period = Column(String, nullable=False)       # e.g. "2024-Q1", "2024-03"
    unit = Column(String, nullable=True)          # e.g. "%", "index"
    source = Column(String, nullable=True)
    fetched_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index("ix_indicator_country_period", "indicator", "country", "period"),
    )
