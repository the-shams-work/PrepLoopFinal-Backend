from __future__ import annotations

from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from .interview import Interview, ScheduledInterview
# from .learning_day import LearningDay
from .week_plan import WeekPlan

__all__ = ("User",)


class User(BaseModel):
    id: UUID = Field(default_factory=uuid4, alias="_id")
    first_name: str
    last_name: Optional[str] = None
    email: str
    password: str
    history: List[Interview] = []
    scheduled_interviews: List[ScheduledInterview] = []
    learning_days: List = []
