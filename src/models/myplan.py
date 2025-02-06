from __future__ import annotations

from pydantic import BaseModel

__all__ = ("MyPlan",)


class MyPlan(BaseModel):
    calories_goal: int | None
    protein_goal: int | None
    carbs_goal: int | None
    fat_goal: int | None

    current_calories_intake: int = 0
    current_protein_intake: int = 0
    current_carbs_intake: int = 0
    current_fat_intake: int = 0

    current_water_intake: int = 0
