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


async def send_otp_email(email: str, otp: int) -> None:
    sender_email = MAIL
    receiver_email = email
    password = PASS

    message = EmailMessage()

    message["From"] = f"PrepLoop <{sender_email}>"
    message["To"] = receiver_email
    message["Subject"] = "PrepLoop Verification Code 🔐"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <body style="margin:0; padding:0; background-color:#f2f6ff; font-family: Arial, sans-serif;">
        
        <div style="max-width:600px; margin:40px auto; background:white; padding:30px; border-radius:12px;">
            
            <!-- Branding -->
            <h1 style="text-align:center; color:#2563eb; margin-bottom:5px;">
                PrepLoop
            </h1>
            <p style="text-align:center; color:#6b7280; margin-top:0;">
                Smart Interview Preparation
            </p>

            <!-- Title -->
            <h2 style="text-align:center; color:#111827;">
                Verify Your Email
            </h2>

            <!-- Message -->
            <p style="text-align:center; color:#374151; font-size:16px;">
                Use the OTP below to continue with <b>PrepLoop</b>.
            </p>

            <!-- OTP Box -->
            <div style="text-align:center; margin:30px 0;">
                <span style="
                    display:inline-block;
                    background:#2563eb;
                    color:white;
                    font-size:30px;
                    letter-spacing:10px;
                    padding:15px 30px;
                    border-radius:10px;
                    font-weight:bold;
                ">
                    {otp}
                </span>
            </div>

            <!-- Info -->
            <p style="text-align:center; color:#6b7280; font-size:14px;">
                This OTP is valid for <b>5 minutes</b>.
            </p>

            <p style="text-align:center; color:#9ca3af; font-size:12px;">
                Do not share this code with anyone.
            </p>

            <hr style="margin:25px 0; border:none; border-top:1px solid #e5e7eb;">

            <!-- Footer -->
            <p style="text-align:center; font-size:12px; color:#9ca3af;">
                Didn’t request this? You can safely ignore this email.
            </p>

            <p style="text-align:center; font-size:12px; color:#d1d5db;">
                © 2026 PrepLoop. All rights reserved.
            </p>

        </div>

    </body>
    </html>
    """

    message.add_alternative(html_content, subtype="html")

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


@router.delete("/delete/{_id}")
async def delete_user_by_id(request: Request, _id: str) -> bool:
    """Delete user details using the user ID"""
    collection = mongo_client["PrepLoop"]["users"]
    await collection.delete_one({"_id": _id})
    return True


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
    await send_otp_email(email, otp)
    return OTP(email=email)


@router.post("/otp/validate")
async def validate_otp(request: Request, otp: OTP):
    """
    Validate OTP given by the server
    """
    status = otp_handler.validate_otp(email=otp.email, otp=otp.otp or -1)
    collection = mongo_client["PrepLoop"]["users"]
    user = await collection.find_one({"email": otp.email})

    if status:
        return user
    
    return None


@router.post("/otp/validate-only")
async def validate_otp_only(request: Request, otp: OTP):
    return otp_handler.validate_otp(email=otp.email, otp=otp.otp or -1)


app.include_router(router)
