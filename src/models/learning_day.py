 from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import BaseModel


class LearningDay(BaseModel):
    id: str
    created_at: datetime
    title: str
    duration: float
    topics: List[str]
    is_completed: bool = False
    is_current: bool = False
