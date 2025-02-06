from __future__ import annotations

from pydantic import BaseModel

from .enums import DifficultyType, ExerciseType

__all__ = ("Exercise",)


class Exercise(BaseModel):
    exercise_type: ExerciseType

    duration: float
    description: str

    tags: list[str]
    level: DifficultyType = DifficultyType.BEGINNER

    exercise_image_name: str
    duration_completed: float = 0
    is_completed: bool = False
