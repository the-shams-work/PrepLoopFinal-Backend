from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

__all__ = ("MyPlan",)


class MyPlan(BaseModel):
    calories_goal: Optional[int]
    protein_goal: Optional[int]
    carbs_goal: Optional[int]
    fat_goal: Optional[int]

    current_calories_intake: int = 0
    current_protein_intake: int = 0
    current_carbs_intake: int = 0
    current_fat_intake: int = 0

    current_water_intake: int = 0
