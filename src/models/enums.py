from __future__ import annotations

from enum import Enum

__all__ = (
    "ExerciseType",
    "MoodType",
    "DifficultyType",
    "PreExistingCondition",
    "Intolerance",
    "DietaryPreference",
    "Country",
)


class ExerciseType(Enum):
    BREATHING = "Breathing"
    STRETCHING = "Stretching"


class MoodType(Enum):
    HAPPY = "Happy"
    SAD = "Sad"
    STRESSED = "Stressed"
    ANGRY = "Angry"


class DifficultyType(Enum):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"


class PreExistingCondition(Enum):
    DIABETES = "diabetes"
    HYPERTENSION = "hypertension"
    PCOS = "pcos"
    ANEMIA = "anemia"
    ASTHMA = "asthma"
    HEART_DISEASE = "heartDisease"
    KIDNEY_DISEASE = "kidneyDisease"


class Intolerance(Enum):
    GLUTEN = "gluten"
    LACTOSE = "lactose"
    EGG = "egg"
    SEAFOOD = "seafood"
    SOY = "soy"
    DAIRY = "dairy"
    WHEAT = "wheat"


class DietaryPreference(Enum):
    VEGETARIAN = "vegetarian"
    NON_VEGETARIAN = "nonVegetarian"
    VEGAN = "vegan"
    PESCETARIAN = "pescetarian"
    FLEXITARIAN = "flexitarian"
    GLUTEN_FREE = "glutenFree"
    KETOGENIC = "ketogenic"
    HIGH_PROTEIN = "highProtein"
    DAIRY_FREE = "dairyFree"


class Country(Enum):
    INDIA = "India"
    USA = "USA"
    UK = "UK"
