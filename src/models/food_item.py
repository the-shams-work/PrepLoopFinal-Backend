from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

__all__ = ("FoodItem",)


class FoodItem(BaseModel):
    id: str = Field(..., title="Food Item ID")
    name: str = Field(..., title="Name", description="Name of the food item")

    calories: Optional[int] = Field(
        0, ge=0, title="Calories", description="Calories in the food item"
    )
    protein: Optional[float] = Field(
        0, ge=0, title="Protein", description="Protein content in the food item"
    )
    carbs: Optional[float] = Field(
        0, ge=0, title="Carbohydrates", description="Carbohydrates in the food item"
    )
    fat: Optional[float] = Field(
        0, ge=0, title="Fat", description="Fat content in the food item"
    )

    consumed: Optional[bool] = Field(
        False, title="Consumed", description="Whether the food item has been consumed"
    )

    image_name: Optional[str] = Field(
        None,
        title="Image Name",
        description="Filename or URL of the image of the food item",
    )
