from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field

from .enums import DifficultyType, ExerciseType

__all__ = ("Exercise",)


class Exercise(BaseModel):
    """
    Represents an exercise with its type, duration, difficulty level, and progress tracking.
    """

    exercise_type: ExerciseType = Field(
        ...,
        title="Type of exercise",
        description="The category of the exercise to be performed.",
        examples=["Breathing"],
    )

    duration: float = Field(
        ...,
        title="Duration",
        description="Total duration of the exercise in seconds.",
        examples=[300],
        gt=0,
    )

    description: str = Field(
        ...,
        title="Description",
        description="A brief explanation of the exercise.",
        examples=["Inhale and exhale"],
    )

    tags: List[str] = Field(
        default=[],
        title="Tags",
        description="Relevant tags to categorize the exercise.",
        examples=[["#relax", "#meditation"]],
    )

    level: DifficultyType = Field(
        default=DifficultyType.BEGINNER,
        title="Level",
        description="Difficulty level of the exercise.",
        examples=["Beginner"],
    )

    exercise_image_name: str = Field(
        ...,
        title="Exercise Image Name",
        description="Filename or URL of the image representing the exercise.",
        examples=["breathing_exercise.png"],
    )

    duration_completed: float = Field(
        default=0,
        title="Duration Completed",
        description="Amount of time (in seconds) the exercise has been completed.",
        examples=[0],
        ge=0,
    )

    is_completed: bool = Field(
        default=False,
        title="Is Completed",
        description="Indicates whether the exercise is completed. It's computed as: `is_completed = duration_completed >= duration - 1`.",
        examples=[False],
    )
