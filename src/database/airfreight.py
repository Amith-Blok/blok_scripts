from src.config.logger import logger
from typing import Dict, List

import pymongo
from src.models.db.airfreight import Airfreight
from src.utils.connection import mongo_test_db, mongo_blok_db


def _get_test_collection():
    db = mongo_test_db()
    return db["airfreights"]

def _get_blok_collection():
    db = mongo_blok_db()
    return db["airfreight"]

def get_test_airports_by_port_code(start_code: str, end_code: str):
    collection = _get_test_collection()
    result = collection.find_one({"start_code": start_code, "end_code": end_code})
    if not result:
        return None

    try:
        return Airfreight(**result)
    except Exception as e:
        logger.error(f"Validation error for port {start_code} and {end_code}: {e}")
        return None


def bulk_upsert_test_airfreights(airfreights: List[Dict]):
    collection = _get_test_collection()
    records = []
    valid_count = 0
    invalid_count = 0

    for airfreight in airfreights:
        try:
            # Validate the data using Pydantic model
            validated_airfreight = Airfreight(**airfreight)
            # Convert back to dict for MongoDB
            validated_dict = validated_airfreight.model_dump()

            filter = {"start_code": validated_dict["start_code"], "end_code": validated_dict["end_code"]}
            update = {"$set": validated_dict}
            records.append({"filter": filter, "update": update, "upsert": True})
            valid_count += 1

        except Exception as e:
            # Log validation errors and skip invalid records
            start_code = airfreight.get("start_code", "unknown")
            end_code = airfreight.get("end_code", "unknown")
            logger.error(f"Validation error for seaport {start_code} and {end_code}: {e}")
            invalid_count += 1
            continue

    # Only proceed with upsert if we have valid records
    if records:
        try:
            collection.bulk_write(
                [
                    pymongo.UpdateOne(op["filter"], op["update"], op["upsert"])
                    for op in records
                ]
            )
            logger.info(f"Successfully upserted {valid_count} valid records")
        except Exception as e:
            logger.error(f"Database error during bulk upsert: {e}")
    else:
        logger.info("No valid records to upsert")

    if invalid_count > 0:
        logger.info(f"Skipped {invalid_count} invalid records")

def bulk_upsert_blok_airfreights(airfreights: List[Dict]):
    collection = _get_blok_collection()
    records = []
    valid_count = 0
    invalid_count = 0
    for airfreight in airfreights:
        try:
            # Validate the data using Pydantic model
            validated_airfreight = Airfreight(**airfreight)
            # Convert back to dict for MongoDB
            validated_dict = validated_airfreight.model_dump()

            filter = {"start_code": validated_dict["start_code"], "end_code": validated_dict["end_code"]}
            update = {"$set": validated_dict}
            records.append({"filter": filter, "update": update, "upsert": True})
            valid_count += 1

        except Exception as e:
            # Log validation errors and skip invalid records
            start_code = airfreight.get("start_code", "unknown")
            end_code = airfreight.get("end_code", "unknown")
            logger.error(f"Validation error for seaport {start_code} and {end_code}: {e}")
            invalid_count += 1
            continue

    # Only proceed with upsert if we have valid records
    if records:
        try:
            collection.bulk_write(
                [
                    pymongo.UpdateOne(op["filter"], op["update"], op["upsert"])
                    for op in records
                ]
            )
            logger.info(f"Successfully upserted {valid_count} valid records")
        except Exception as e:
            logger.error(f"Database error during bulk upsert: {e}")
    else:
        logger.info("No valid records to upsert")

    if invalid_count > 0:
        logger.info(f"Skipped {invalid_count} invalid records")

def delete_test_airfreights():
    collection = _get_test_collection()
    collection.delete_many({})
