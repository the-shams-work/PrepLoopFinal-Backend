from __future__ import annotations


from bson import ObjectId
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, EmailStr
from pymongo.results import InsertOneResult

from src.app import app, mongo_client
from src.models import User

__all__ = ("create_user", "update_user", "fetch_user")

router = APIRouter(prefix="/user", tags=["User"])


class UserCredential(BaseModel):
    email: str
    password: str


async def _fetch_user(*, email: str, password: str) -> User:
    collection = mongo_client["PrepLoop"]["users"]
    user = await collection.find_one({"email": email, "password": password})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return User.model_validate(user)


async def user_exists(*, email: str) -> bool:
    collection = mongo_client["PrepLoop"]["users"]
    return await collection.count_documents({"email": email}) > 0


@router.post(
    "/create",
    response_model=User,
    responses={400: {"description": "User already exists"}, 422: {}},
)
async def create_user(request: Request, data: User) -> User:
    if await user_exists(email=data.email):
        raise HTTPException(status_code=400, detail="User already exists")

    collection = mongo_client["PrepLoop"]["users"]
    sendable_data = data.model_dump(mode="json")
    sendable_data["_id"] = sendable_data.pop("id")

    await collection.insert_one(sendable_data)

    return data

@router.post(
    "/fetch",
    response_model=User,
    responses={404: {"description": "User not found"}, 422: {}},
)
async def fetch_user(request: Request, data: UserCredential):
    """
    Fetch user details using email and password.
    """
    return await _fetch_user(email=data.email, password=data.password)


@router.get(
    "/fetch/{_id}",
    response_model=User,
    responses={404: {"description": "User not found"}, 422: {}},
)
async def fetch_user_by_id(request: Request, _id: str) -> User:
    """
    Fetch user details using the user ID.
    """
    collection = mongo_client["PrepLoop"]["users"]
    user = await collection.find_one({"_id": _id})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return User.model_validate(user)


@router.put(
    "/update/{_id}",
    response_model=User,
    responses={
        400: {"description": "Invalid update operation"},
        404: {"description": "User not found"},
        422: {},
    },
)
async def update_user(request: Request, user: User) -> User:
    """
    Update user details based on the user ID.
    """
    collection = mongo_client["PrepLoop"]["users"]
    try:
        user_dumped = user.model_dump(mode="json")
        user_dumped.pop("_id", None)
        result = await collection.update_one(
            {"_id": str(user.id)},
            {"$set": user_dumped},
        )
        if result.modified_count == 0:
            raise HTTPException(
                status_code=404, detail="User not found or no changes applied"
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return user


app.include_router(router)
