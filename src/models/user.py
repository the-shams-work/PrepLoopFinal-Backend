from __future__ import annotations

from datetime import datetime
from typing import List, Optional

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
    exercise: List[Exercise]


class User(BaseModel):
    id: str
    first_name: str
    last_name: str

    email_address: str
    password: str

    country_code: str = "+91"
    country: Country = Country.INDIA

    phone_number: str

    medical_data: Optional[UserMedical]
    mood: Optional[MoodType]

    exercises: List[Exercise] = []
    plan: Optional[MyPlan]

    history: List[History] = []

    created_at: datetime
    updated_at: Optional[datetime] = None


class UserMedical(BaseModel):
    date_of_birth: datetime
    height: float
    pre_pregnancy_weight: float
    current_weight: float

    due_date: Optional[datetime]
    pre_existing_conditions: List[PreExistingCondition] = []
    food_intolerances: List[Intolerance] = []
    dietary_preferences: List[DietaryPreference] = []
