from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from .enums import (
    Country,
    DietaryPreference,
    Intolerance,
    MoodType,
    PreExistingCondition,
)
from .exercise import Exercise
from .myplan import MyPlan

__all__ = ("User", "UserMedical", "History")


class History(BaseModel):
    date: datetime
    plan: MyPlan
    exercise: list[Exercise]


class User(BaseModel):
    id: str
    first_name: str
    last_name: str

    email_address: str
    password: str

    country_code: str = "+91"
    country: Country = Country.INDIA

    phone_number: str

    mood: MoodType | None

    exercise: list[Exercise] = []
    plan: MyPlan | None

    history: list[History] = []

    created_at: datetime
    updated_at: datetime | None = None


class UserMedical(BaseModel):
    date_of_birth: datetime
    height: float
    pre_pregnancy_weight: float
    current_weight: float

    due_date: datetime | None
    pre_existing_conditions: list[PreExistingCondition] = []
    food_intolerances: list[Intolerance] = []
    dietary_preferences: list[DietaryPreference] = []

