from __future__ import annotations

from time import perf_counter
from typing import Literal

from pydantic import BaseModel, Field

from src.app import app, mongo_client

__all__ = ("ping", "root")


class PingResponse(BaseModel):
    success: bool = Field(
        ...,
        description="Whether the ping was successful. True if database is reachable, False otherwise.",
    )
    ping: Literal["pong"] = Field(
        "pong",
        description="The response to the ping request. Should be 'pong' if successful.",
    )
    response_time: float = Field(
        ...,
        description="The time taken to receive a response from the database in seconds.",
    )


class RootResponse(BaseModel):
    success: Literal[True] = Field(
        True,
        description="Whether the request was successful. Should always be True.",
        frozen=True,
    )
    message: Literal["Welcome to PrepLoop API!"] = Field(
        "Welcome to PrepLoop API!",
        description="A welcome message for the API.",
        frozen=True,
    )


@app.get("/ping")
async def ping() -> PingResponse:
    """
    Check if the database is reachable. Returns the response time if successful.
    """

    start = perf_counter()
    success = True
    try:
        _ = await mongo_client.server_info()
    except Exception:
        success = False

    fin = perf_counter()

    return PingResponse(success=success, ping="pong", response_time=fin - start)


@app.get("/")
async def root() -> RootResponse:
    """
    A welcome message for the API. This endpoint is used to check if the API is running; it should always return True.
    """
    return RootResponse(success=True, message="Welcome to PrepLoop API!")
