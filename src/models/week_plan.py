from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from .enums import Duration

__all__ = ("WeekPlan",)


class WeekPlan(BaseModel):
    duration: Duration
    subject: str
    topics: List[str] = []
    date: datetime = Field(default_factory=datetime.utcnow)
