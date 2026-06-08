from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class IndicatorBase(BaseModel):
    indicator: str
    country: str = "US"
    value: float
    period: str
    unit: Optional[str] = None
    source: Optional[str] = None


class IndicatorCreate(IndicatorBase):
    pass


class IndicatorResponse(IndicatorBase):
    id: int
    fetched_at: datetime

    class Config:
        from_attributes = True


class IndicatorListResponse(BaseModel):
    total: int
    data: List[IndicatorResponse]


class SummaryItem(BaseModel):
    indicator: str
    country: str
    latest_value: float
    latest_period: str
    unit: Optional[str]
    change: Optional[float] = Field(None, description="Change from previous period")


class FetchResponse(BaseModel):
    message: str
    records_saved: int
    indicator: str
