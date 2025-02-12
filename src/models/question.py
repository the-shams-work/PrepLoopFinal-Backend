from __future__ import annotations

from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

__all__ = ("Question",)


class Question(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    question: str
    correct_answer: str
    user_answer: Optional[str] = None
    accuracy: float = 0.0
