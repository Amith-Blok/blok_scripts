from typing import Dict, List
from pydantic import ValidationError
import pymongo
from src.utils.connection import mongo_test_db, mongo_blok_db
from src.utils.json_util import load_json
from src.models.db.lines import Lines
from src.config.logger import logger


def _get_test_collection():
    db = mongo_test_db()
    return db["lines_rate"]


def _get_blok_collection():
    db = mongo_blok_db()
    return db["lines_rates"]


def get_blok_line_by_codes(start_code: str, end_code: str):
    lines_blok_collection = _get_blok_collection()
    result = lines_blok_collection.find_one(
        {"start_code": start_code, "end_code": end_code}
    )
    if not result:
        return None
    return dict(result)


def get_test_lines():
    lines_collection = _get_test_collection()
    result = lines_collection.find_one({})
    if not result:
        return None
    return dict(result)


def upsert_test_lines_by_path(path: str):
    lines_collection = _get_test_collection()
    lines_data = load_json(path=path)
    try:
        [Lines.model_validate(lines) for lines in lines_data]
    except ValidationError as e:
        print(f"Line Json is not valid: {e}")
    records = []
    for lines in lines_data:
        start_code = lines.get("start_code", "")
        end_code = lines.get("end_code", "")
        query = {"start_code": start_code, "end_code": end_code}
        update = {"$set": lines}
        records.append({"filter": query, "update": update, "upsert": True})
    lines_collection.bulk_write(
        [pymongo.UpdateOne(op["filter"], op["update"], op["upsert"]) for op in records]
    )

def delete_test_lines():
    lines_collection = _get_test_collection()
    lines_collection.delete_many({})
    logger.info("Finished:Delete Test Lines")

def upsert_test_lines(Lines_record: List[Dict]):
    lines_collection = _get_test_collection()
    records = []
    for lines in Lines_record:
        start_code = lines["start_code"]
        end_code = lines["end_code"]
        query = {"start_code": start_code, "end_code": end_code}
        update = {"$set": lines}
        records.append({"filter": query, "update": update, "upsert": True})
    lines_collection.bulk_write(
        [pymongo.UpdateOne(op["filter"], op["update"], op["upsert"]) for op in records]
    )
    logger.info("Finished:Bulk Write Completed")
