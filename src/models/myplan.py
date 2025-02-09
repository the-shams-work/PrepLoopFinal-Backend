from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from .enums import MealType
from .food_item import FoodItem

__all__ = ("MyPlan",)


class MyPlan(BaseModel):
    """
    Represents a user's nutrition and hydration tracking plan.
    """

    calories_goal: Optional[int] = Field(
        0, ge=0, description="Daily target for calorie intake."
    )
    protein_goal: Optional[int] = Field(
        0, ge=0, description="Daily target for protein intake (grams)."
    )
    carbs_goal: Optional[int] = Field(
        0, ge=0, description="Daily target for carbohydrate intake (grams)."
    )
    fat_goal: Optional[int] = Field(
        0, ge=0, description="Daily target for fat intake (grams)."
    )

    current_calories_intake: int = Field(
        0, ge=0, description="Current amount of calories consumed."
    )
    current_protein_intake: int = Field(
        0, ge=0, description="Current amount of protein consumed (grams)."
    )
    current_carbs_intake: int = Field(
        0, ge=0, description="Current amount of carbohydrates consumed (grams)."
    )
    current_fat_intake: int = Field(
        0, ge=0, description="Current amount of fat consumed (grams)."
    )

    current_water_intake: int = Field(
        0, ge=0, description="Current amount of water consumed (milliliters)."
    )

    meals: dict[MealType, list[FoodItem]] = Field(
        {}, description="Dictionary of meals with their food items."
    )
