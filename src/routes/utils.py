from __future__ import annotations

from time import perf_counter
from fastapi import HTTPException, Request
from src.app import app, mongo_client
from src.models import User

__all__ = ("create_user", "update_user", "get_user")
