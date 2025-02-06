from __future__ import annotations

import os
import secrets
from typing import TYPE_CHECKING, Any

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from src.app import app, mongo_client

if TYPE_CHECKING:
    from pymongo.results import (
        DeleteResult,
        InsertManyResult,
        InsertOneResult,
        UpdateResult,
    )

    from type import MongoCollection

__all__ = (
    "find_one",
    "find_all",
    "insert_one",
    "insert_many",
    "update",
    "update_many",
    "delete_one",
    "delete_many",
    "replace_one",
)

ADMIN_USERNAME = os.environ["ADMIN_USERNAME"]
ADMIN_PASSWORD = os.environ["ADMIN_PASSWORD"]

security = HTTPBasic()

router = APIRouter(prefix="/collection", tags=["CRUD"])


def validate_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, ADMIN_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, ADMIN_PASSWORD)

    if not (correct_username and correct_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    return credentials.username


async def get_query_params(request: Request):
    if request.method == "GET":
        return {k: v for k, v in request.query_params.items()}
    elif request.method in {"POST", "PUT", "DELETE"}:
        data = await request.json()
        return {k: v for k, v in data.items()} if data else None
    return None


def serialize_doc(bson_document: Any):
    if isinstance(bson_document, list):
        return [serialize_single_doc(doc) for doc in bson_document]
    return serialize_single_doc(bson_document)


def serialize_single_doc(bson_document: Any):
    def convert_bson_types(obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, dict):
            return {key: convert_bson_types(value) for key, value in obj.items()}
        if isinstance(obj, list):
            return [convert_bson_types(item) for item in obj]
        return obj

    return convert_bson_types(bson_document)


async def handle_find_one(collection: MongoCollection, query: dict):
    result = await collection.find_one(query)
    return {"success": True, "result": serialize_doc(result)}


async def handle_find_all(collection: MongoCollection, query: dict):
    cursor = collection.find(query)
    result = [doc async for doc in cursor]
    return {"success": True, "result": serialize_doc(result)}


async def handle_insert_one(collection: MongoCollection, query: dict):
    result: InsertOneResult = await collection.insert_one(query)
    return {"success": True, "inserted_id": str(result.inserted_id)}


async def handle_insert_many(collection: MongoCollection, query):
    result: InsertManyResult = await collection.insert_many(query)
    return {"success": True, "inserted_ids": [str(oid) for oid in result.inserted_ids]}


async def handle_update(collection: MongoCollection, query: dict):
    filter_criteria = query.get("filter")
    update_criteria = query.get("update")

    if filter_criteria is None or update_criteria is None:
        raise HTTPException(status_code=400, detail="Missing filter or update data")

    result: UpdateResult = await collection.update_one(filter_criteria, update_criteria)

    if result.matched_count == 0:
        return {"success": False, "message": "No document matched the query"}

    return {
        "success": True,
        "matched_count": result.matched_count,
        "modified_count": result.modified_count,
    }


async def handle_update_many(collection: MongoCollection, query: dict):
    filter_criteria = query.get("filter")
    update_criteria = query.get("update")

    if filter_criteria is None or update_criteria is None:
        raise HTTPException(status_code=400, detail="Missing filter or update data")

    result: UpdateResult = await collection.update_many(
        filter_criteria, update_criteria
    )

    if result.matched_count == 0:
        return {"success": False, "message": "No documents matched the query"}

    return {
        "success": True,
        "matched_count": result.matched_count,
        "modified_count": result.modified_count,
    }


async def handle_delete_one(collection: MongoCollection, query: dict):
    filter_criteria = query.get("filter")

    if not filter_criteria:
        raise HTTPException(status_code=400, detail="Missing filter data")

    result: DeleteResult = await collection.delete_one(filter_criteria)

    if result.deleted_count == 0:
        return {"success": False, "message": "No document matched the query to delete"}

    return {"success": True, "deleted_count": result.deleted_count}


async def handle_delete_many(collection: MongoCollection, query: dict):
    filter_criteria = query.get("filter")

    if not filter_criteria:
        raise HTTPException(status_code=400, detail="Missing filter data")

    result: DeleteResult = await collection.delete_many(filter_criteria)

    if result.deleted_count == 0:
        return {"success": False, "message": "No documents matched the query to delete"}

    return {"success": True, "deleted_count": result.deleted_count}


async def handle_replace_one(collection: MongoCollection, query: dict):
    filter_criteria = query.get("filter")
    replacement = query.get("replacement")

    if not filter_criteria or not replacement:
        raise HTTPException(
            status_code=400, detail="Missing filter or replacement data"
        )

    result = await collection.replace_one(filter_criteria, replacement)

    if result.matched_count == 0:
        return {"success": False, "message": "No document matched the query"}

    return {
        "success": True,
        "matched_count": result.matched_count,
        "modified_count": result.modified_count,
    }


OPERATION_MAP = {
    "find_one": handle_find_one,
    "find_all": handle_find_all,
    "insert_one": handle_insert_one,
    "insert_many": handle_insert_many,
    "update": handle_update,
    "update_many": handle_update_many,
    "delete_one": handle_delete_one,
    "delete_many": handle_delete_many,
    "replace_one": handle_replace_one,
}


async def handle_request(collection_name: str, request: Request, operation: str):
    collection = mongo_client["MomCare"][collection_name]
    query = await get_query_params(request)

    if query is None:
        return {"success": False, "message": "Bad Request"}

    try:
        operation_func = OPERATION_MAP.get(operation)
        if operation_func:
            return await operation_func(collection, query)
        else:
            RuntimeError("Invalid operation")
    except Exception as e:
        return {"success": False, "message": str(e)}


@router.post("/{collection_name}/find-one")
async def find_one(
    collection_name: str,
    request: Request,
    credentials: HTTPBasicCredentials = Depends(validate_credentials),
):
    return await handle_request(collection_name, request, "find_one")


@router.post("/{collection_name}/find-all")
async def find_all(
    collection_name: str,
    request: Request,
    credentials: HTTPBasicCredentials = Depends(validate_credentials),
):
    return await handle_request(collection_name, request, "find_all")


@router.put("/{collection_name}/insert-one")
async def insert_one(
    collection_name: str,
    request: Request,
    credentials: HTTPBasicCredentials = Depends(validate_credentials),
):
    return await handle_request(collection_name, request, "insert_one")


@router.put("/{collection_name}/insert-many")
async def insert_many(
    collection_name: str,
    request: Request,
    credentials: HTTPBasicCredentials = Depends(validate_credentials),
):
    return await handle_request(collection_name, request, "insert_many")


@router.put("/{collection_name}/update")
async def update(
    collection_name: str,
    request: Request,
    credentials: HTTPBasicCredentials = Depends(validate_credentials),
):
    return await handle_request(collection_name, request, "update")


@router.put("/{collection_name}/update-many")
async def update_many(
    collection_name: str,
    request: Request,
    credentials: HTTPBasicCredentials = Depends(validate_credentials),
):
    return await handle_request(collection_name, request, "update_many")


@router.delete("/{collection_name}/delete-one")
async def delete_one(
    collection_name: str,
    request: Request,
    credentials: HTTPBasicCredentials = Depends(validate_credentials),
):
    return await handle_request(collection_name, request, "delete_one")


@router.delete("/{collection_name}/delete-many")
async def delete_many(
    collection_name: str,
    request: Request,
    credentials: HTTPBasicCredentials = Depends(validate_credentials),
):
    return await handle_request(collection_name, request, "delete_many")


@router.put("/{collection_name}/replace-one")
async def replace_one(
    collection_name: str,
    request: Request,
    credentials: HTTPBasicCredentials = Depends(validate_credentials),
):
    return await handle_request(collection_name, request, "replace_one")


app.include_router(router)
