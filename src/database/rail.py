from ast import Dict
from typing import List

import pymongo
from src.models.db.port import Port
from src.utils.connection import mongo_test_db
from src.config.logger import logger


def _get_test_collection():
    db = mongo_test_db()
    return db["rail"]


def bulk_upsert_test_rail(rails: List[Dict]):
    collection = _get_test_collection()
    records = []
    valid_count = 0
    invalid_count = 0

    for rail in rails:
        try:
            # Validate the data using Pydantic model
            validated_rail = Port(**rail)
            # Convert back to dict for MongoDB
            validated_dict = validated_rail.model_dump()

            filter = {"port_code": validated_dict["port_code"]}
            update = {"$set": validated_dict}
            records.append({"filter": filter, "update": update, "upsert": True})
            valid_count += 1

        except Exception as e:
            # Log validation errors and skip invalid records
            port_code = rail.get("port_code", "unknown")
            print(f"Validation error for rail {port_code}: {e}")
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


def delete_test_rail():
    collection = _get_test_collection()
    collection.delete_many({})
    logger.info("Successfully deleted all records from test rail collection")

