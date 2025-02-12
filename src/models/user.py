from __future__ import annotations

from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from .interview import Interview
from .week_plan import WeekPlan

__all__ = ("User",)


class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    mongo_id: Optional[str] = Field(None, alias="_id")
    first_name: str
    last_name: Optional[str] = None
    email: str
    password: str
    history: List[Interview] = []
    week_plan: Optional[WeekPlan] = None
