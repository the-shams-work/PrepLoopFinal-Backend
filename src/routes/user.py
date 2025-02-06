from __future__ import annotations

from datetime import datetime
from time import perf_counter
from typing import TYPE_CHECKING

from fastapi import APIRouter, HTTPException, Request
from pymongo.results import InsertOneResult

from src.app import app, mongo_client
from src.models import User
from type import MongoCollection

__all__ = ("create_user", "update_user", "fetch_user")

router = APIRouter(prefix="/user", tags=["User"])


async def _fetch_user(*, email: str, password: str) -> User:
    collection = mongo_client["MomCare"]["users"]
    user = await collection.find_one(
        {"email_address": email, "password": password}, {"password": 0, "_id": 0}
    )
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user["id"] = str(user["_id"])
    return User.model_validate(user)


async def user_exists(*, email: str) -> bool:
    collection = mongo_client["MomCare"]["users"]
    return await collection.count_documents({"email_address": email}) > 0


@router.post("/create")
async def create_user(request: Request, data: User):
    if await user_exists(email=data.email_address):
        raise HTTPException(status_code=400, detail="User already exists")

    collection = mongo_client["MomCare"]["users"]
    result: InsertOneResult = await collection.insert_one(dict(data))

    return {"success": True, "inserted_id": str(result.inserted_id)}


@router.get("/fetch")
async def fetch_user(request: Request, email: str, password: str):
    user = await _fetch_user(email=email, password=password)
    return {"success": True, "user": dict(user)}


@router.put("/update")
async def update_user(
    request: Request, email: str, password: str, update_criteria: dict
):
    collection = mongo_client["MomCare"]["users"]
    result = await collection.update_one(
        {"email_address": email, "password": password}, update_criteria
    )

    return {"success": True, "modified_count": result.modified_count}


app.include_router(router)
