from __future__ import annotations

import os

from dotenv import load_dotenv
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

URI = os.getenv("MONGODB_URI")

if URI is None:
    raise ValueError("MONGODB_URI is not set")

mongo_client = AsyncIOMotorClient(URI, document_class=dict)
database = mongo_client["MomCare"]

app = FastAPI(
    title="MomCare API Documentation",
    description="API documentation for the MomCare project - a health and fitness application. The API is used to manage users, exercises, and plans.",
    version="0.1",
    contact={
        "name": "Ritik Ranjan",
        "url": "https://github.com/rtk-rnjn",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

from .routes import *  # noqa: E402, F401, F403
