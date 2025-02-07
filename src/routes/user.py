from __future__ import annotations

from bson import ObjectId
from fastapi import APIRouter, HTTPException, Request
from pymongo.results import InsertOneResult

from src.app import app, mongo_client
from src.models import User

__all__ = ("create_user", "update_user", "fetch_user")

router = APIRouter(prefix="/user", tags=["User"])


async def _fetch_user(*, email: str, password: str) -> User:
    collection = mongo_client["MomCare"]["users"]
    user = await collection.find_one(
        {"email_address": email, "password": password}, {"password": 0}
    )
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user["password"] = "HIDDEN FOR SECURITY REASONS"
    return User.model_validate(user)


async def user_exists(*, email: str) -> bool:
    collection = mongo_client["MomCare"]["users"]
    return await collection.count_documents({"email_address": email}) > 0


@router.post("/create")
async def create_user(request: Request, data: User) -> dict:
    if await user_exists(email=data.email_address):
        raise HTTPException(status_code=400, detail="User already exists")

    collection = mongo_client["MomCare"]["users"]
    sendable_data = data.model_dump(mode="json")
    result: InsertOneResult = await collection.insert_one(dict(data))

    return {"success": True, "inserted_id": str(result.inserted_id)}


@router.get("/fetch")
async def fetch_user(request: Request, email: str, password: str) -> User:
    return await _fetch_user(email=email, password=password)


@router.get("/fetch/{_id}")
async def fetch_user_by_id(request: Request, _id: str) -> User:
    collection = mongo_client["MomCare"]["users"]
    user = await collection.find_one({"_id": ObjectId(_id)}, {"password": 0})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return User.model_validate(user)


@router.put("/update")
async def update_user(
    request: Request, email: str, password: str, update_criteria: dict
):
    collection = mongo_client["MomCare"]["users"]
    try:
        result = await collection.update_one(
            {"email_address": email, "password": password}, update_criteria
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"success": True, "modified_count": result.modified_count}


app.include_router(router)
