from __future__ import annotations

from typing import List

from pydantic import BaseModel

__all__ = ("SubjectData",)


class SubjectData(BaseModel):
    subject: str
    topics: List[str]
