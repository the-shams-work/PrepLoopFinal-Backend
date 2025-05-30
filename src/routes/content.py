from __future__ import annotations

from fastapi import APIRouter, Request
from src.utils import GoogleGenerativeAIHandler
from pydantic import BaseModel
from src.app import app

class ClientReqeust(BaseModel):
    number_of_questions: int
    selected_topics: list[str]

router = APIRouter(prefix="/content", tags=["CONTENT"])
genai = GoogleGenerativeAIHandler()


@router.post("/questions")
async def fetch_questions(request: Request, data: ClientReqeust):
    return genai.generate_questions(data.number_of_questions, *data.selected_topics)

app.include_router(router)
