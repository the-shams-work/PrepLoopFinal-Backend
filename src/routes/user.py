from __future__ import annotations

import os
from email.message import EmailMessage
from typing import Optional

from aiosmtplib import send
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, EmailStr

from src.app import app, mongo_client
from src.models import User
from src.utils import OTPHandler

__all__ = ("create_user", "update_user", "fetch_user")

router = APIRouter(prefix="/user", tags=["User"])
otp_handler = OTPHandler(cache_size=2**10)

MAIL = os.environ["MAIL"]
PASS = os.environ["PASS"]


class UserCredential(BaseModel):
    email: str
    password: str


class OTP(BaseModel):
    email: str
    otp: Optional[int] = None


async def send_email(email: str, body: str):
    sender_email = MAIL
    receiver_email = email
    password = PASS

    message = EmailMessage()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "OTP"
    message.set_content(body)

    await send(
        message,
        hostname="smtp.gmail.com",
        port=465,
        username=sender_email,
        password=password,
        use_tls=True,
    )


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


@router.post(
    "/otp/generate",
    response_model=OTP,
)
async def generate_otp(request: Request, email: EmailStr) -> OTP:
    """
    Generate OTP based on email
    """
    otp = otp_handler.generate_otp(email=email)
    await send_email(email, f"YOUR OTP: {otp}")
    return OTP(email=email)


@router.post("/otp/validate", response_model=bool)
async def validate_otp(request: Request, otp: OTP) -> bool:
    """
    Validate OTP given by the server
    """
    return otp_handler.validate_otp(email=otp.email, otp=otp.otp or -1)


app.include_router(router)
