from __future__ import annotations

from fastapi import APIRouter, Request
from src.utils import GoogleGenerativeAIHandler
from src.app import app

router = APIRouter(prefix="/content", tags=["CONTENT"])
genai = GoogleGenerativeAIHandler()

@router.post("/questions")
async def fetch_questions(request: Request, number_of_questions: int, selected_topics: list[str]):
    return 


app.include_router(router)
