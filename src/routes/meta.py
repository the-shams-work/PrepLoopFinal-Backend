from __future__ import annotations

from time import perf_counter

from src.app import app, mongo_client

__all__ = ("ping",)


@app.get("/ping")
async def ping():
    start = perf_counter()
    _ = await mongo_client.server_info()
    fin = perf_counter()

    return {"success": True, "ping": "pong", "response_time": fin - start}


@app.get("/")
async def root():
    return {"success": True, "message": "Welcome to MomCare API!"}
