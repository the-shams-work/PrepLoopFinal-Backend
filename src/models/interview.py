from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from .enums import InterviewFlag
from .question import Question

__all__ = ("Interview",)


class ScheduledInterview(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    subject: str
    topics: List[str] = []
    duration: float
    date: datetime


class Interview(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    subject: str
    topics: List[str] = []
    questions: List[Question]
    start_date: datetime
    end_date: datetime
    overall_score: float = 0.0
    eye_contact_percentage: float = 0.0
    flag: Optional[InterviewFlag] = None
    video_url: Optional[str] = None
    is_completed: Optional[bool] = False
