from typing import Dict, List
from src.models.db.distination_charges import DestinationCharges
from src.utils.connection import mongo_test_db
from src.config.logger import logger
import pymongo


def _get_test_collection():
    db = mongo_test_db()
    return db["destination_charges"]

def get_test_destination_charges_by_port_code(end_code: str):
    collection = _get_test_collection()
    result = collection.find_one({"port_code": end_code})
    if not result:
        return None

    try:
        return DestinationCharges(**result)
    except Exception as e:
        print(f"Validation error for port {end_code}: {e}")
        return None

def bulk_upsert_test_destination_charges(destination_charges: List[Dict]):
    """
    Bulk upsert destination charges into the database.
    """
    collection = _get_test_collection()
    records = []
    valid_count = 0
    invalid_count = 0

    for destination_charge in destination_charges:
        try:
            # Validate the data using Pydantic model
            validated_destination_charge = DestinationCharges(**destination_charge)     
            # Convert back to dict for MongoDB
            validated_dict = validated_destination_charge.model_dump()

            filter = {"port_code": validated_dict["port_code"]}
            update = {"$set": validated_dict}
            records.append({"filter": filter, "update": update, "upsert": True})
            valid_count += 1

        except Exception as e:
            # Log validation errors and skip invalid records
            port_code = destination_charge.get("port_code", "unknown")
            print(f"Validation error for port {port_code}: {e}")
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
def delete_test_destination_charges():
    collection = _get_test_collection()
    collection.delete_many({})
    logger.info("Finished deleting all destination charges from test db")   