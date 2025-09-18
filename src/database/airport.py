from typing import Dict, List

import pymongo
from src.models.db.airport import Airport
from src.utils.connection import mongo_test_db
import folium


def _get_test_collection():
    db = mongo_test_db()
    return db["airports"]


def get_test_airports_by_port_code(port_code: str):
    collection = _get_test_collection()
    result = collection.find_one({"port_code": port_code})
    if not result:
        return None

    try:
        return Airport(**result)
    except Exception as e:
        print(f"Validation error for port {port_code}: {e}")
        return None


def bulk_upsert_test_airports(airports: List[Dict]):
    collection = _get_test_collection()
    records = []
    valid_count = 0
    invalid_count = 0

    for airport in airports:
        try:
            # Validate the data using Pydantic model
            validated_airport = Airport(**airport)
            # Convert back to dict for MongoDB
            validated_dict = validated_airport.model_dump()

            filter = {"port_code": validated_dict["port_code"]}
            update = {"$set": validated_dict}
            records.append({"filter": filter, "update": update, "upsert": True})
            valid_count += 1

        except Exception as e:
            # Log validation errors and skip invalid records
            port_code = airport.get("port_code", "unknown")
            print(f"Validation error for seaport {port_code}: {e}")
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
            print(f"Successfully upserted {valid_count} valid records")
        except Exception as e:
            print(f"Database error during bulk upsert: {e}")
    else:
        print("No valid records to upsert")

    if invalid_count > 0:
        print(f"Skipped {invalid_count} invalid records")


def delete_test_airports():
    collection = _get_test_collection()
    collection.delete_many({})


def create_airport_map():
    collection = _get_test_collection()
    m = folium.Map(location=[20, 0], zoom_start=2)  # center of world

    total_docs = collection.count_documents({})
    print(f"Total documents in collection: {total_docs}")

    marked_count = 0
    skipped_count = 0

    for doc in collection.find():
        try:
            # Check if location and coordinates exist
            if "location" not in doc:
                print(
                    f"Skipping document without location: {doc.get('port_name', 'Unknown')}"
                )
                skipped_count += 1
                continue

            if "coordinates" not in doc["location"]:
                print(
                    f"Skipping document without coordinates: {doc.get('port_name', 'Unknown')}"
                )
                skipped_count += 1
                continue

            coords = doc["location"]["coordinates"]

            # Check if coordinates are valid
            if not isinstance(coords, list) or len(coords) != 2:
                print(
                    f"Skipping document with invalid coordinates format: {doc.get('port_name', 'Unknown')} - {coords}"
                )
                skipped_count += 1
                continue

            # Check if coordinates are numbers
            if not (
                isinstance(coords[0], (int, float))
                and isinstance(coords[1], (int, float))
            ):
                print(
                    f"Skipping document with non-numeric coordinates: {doc.get('port_name', 'Unknown')} - {coords}"
                )
                skipped_count += 1
                continue

            port_name = doc.get("port_name", "Unknown")

            folium.Marker(
                location=[coords[1], coords[0]],  # lat, lon
                popup=port_name,
            ).add_to(m)

            marked_count += 1

        except Exception as e:
            print(f"Error processing document {doc.get('port_name', 'Unknown')}: {e}")
            skipped_count += 1
            continue

    print(f"Successfully marked {marked_count} seaports")
    print(f"Skipped {skipped_count} documents")

    m.save("ports_map.html")
