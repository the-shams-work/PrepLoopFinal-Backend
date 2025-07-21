from __future__ import annotations

import json
import os
import random
from typing import List, Optional

import lru
from datetime import datetime, timedelta

from dotenv import load_dotenv
from google import genai
from google.genai.types import Content, GenerateContentConfig, Part
from pydantic import BaseModel

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


class _Question(BaseModel):
    question: str
    correct_answer: str


class _Response(BaseModel):
    questions: List[_Question]


class OTPHandler:
    def __init__(self, cache_size: int = 2**10):
        self.cache_size = cache_size
        self.lru = lru.LRU(self.cache_size)

    def _generate_otp(self) -> int:
        return random.randint(100_000, 999_999)

    def generate_otp(self, *, email: str) -> int:
        self.lru[email] = self._generate_otp()
        return self.lru[email]

    def validate_otp(self, *, email: str, otp: int) -> bool:
        try:
            self.lru[email]
            validate = self.lru[email] == otp
            if validate:
                del self.lru[email]

            return validate
        except KeyError:
            return False


SYSTEM_INSTRUCTION = """
You are a professional Intervier with experience of 15yr, and have expertise in many different fields. You will be given the data of User. You need to take mock interview. of that user. You will be given Selected number of subject.

**Crucial Instructions:**
1. **Strict JSON Output:** You MUST respond exclusively with valid JSON data, adhering to the specified format below. No additional text, explanations, or conversational elements are allowed outside of the JSON structure.
2. **Question Quality:** Generate questions that are easy to medium in difficulty, requiring in-depth knowledge and understanding of the provided topics. Ensure the answers are based on the most current, well-researched, and accurate information.
3. **Error Handling (Implicit):** If you encounter any ambiguity or cannot generate questions based on the provided input, return an empty "questions" array within the JSON structure.
4. **Make Sure that only theoratical question should be presence which required good lenght of answer.**
5. **Avoid Code Examples:** Do not include any code snippets or examples within the questions or answers. Focus solely on theoretical concepts and explanations.
6. **Formatting Excellence:** Ensure all questions and answers are well-formatted, using proper grammar, punctuation, and clear, concise language. Structure answers to be comprehensive and readable, ideally as full paragraphs when necessary.
"""


class GoogleGenerativeAIHandler:
    CACHE_DURATION = timedelta(minutes=10)

    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        # Store (response, timestamp) for each key
        self._temp = {}

    def generate_questions(
        self, number_of_questions: int, *selected_topics: str
    ) -> Optional[_Response]:
        
        current_time = datetime.utcnow()
        cached = self._temp.get(selected_topics)

        if cached:
            response, timestamp = cached
            if current_time - timestamp < self.CACHE_DURATION:
                return response
            else:
                del self._temp[selected_topics]

        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=[
                    Content(
                        parts=[
                            Part.from_text(text=f"Prepared topics: {selected_topics}"),
                        ]
                    )
                ],
                config=GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION
                    + "\n"
                    + f"Total Number of questions need: {number_of_questions}",
                    response_mime_type="application/json",
                    response_schema=_Response,
                ),
            )

            if response:
                response = _Response(**json.loads(response.text or "{}"))
                self._temp[selected_topics] = (response, current_time)
                return response

        except Exception as e:
            return None

        return None
