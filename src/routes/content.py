from __future__ import annotations

from fastapi import APIRouter, Request, HTTPException
from src.utils import GoogleGenerativeAIHandler
from src.app import app, mongo_client
from src.models import User

router = APIRouter(prefix="/content", tags=["CONTENT"])
genai = GoogleGenerativeAIHandler()


@router.post("/questions")
async def fetch_questions(request: Request, number_of_questions: int, selected_topics: list[str]):
    return genai.generate_questions(number_of_questions, *selected_topics)

app.include_router(router)
