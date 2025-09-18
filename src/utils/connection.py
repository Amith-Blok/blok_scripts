from pymongo import MongoClient
from src.config.settings import (
    MONGO_DB_CONNECTION_STRING,
    MONGO_BLOK_DATABASE,
    MONGO_TEST_DATABASE,
)


def mongo_test_db():
    client = MongoClient(MONGO_DB_CONNECTION_STRING)

    if not MONGO_DB_CONNECTION_STRING:
        raise ValueError("missing MONGO_DB_CONNECTION_STRING")
    if not MONGO_TEST_DATABASE:
        raise ValueError("missing MONGO_DATABASE env")

    return client[MONGO_TEST_DATABASE]


def mongo_blok_db():
    client = MongoClient(MONGO_DB_CONNECTION_STRING)

    if not MONGO_DB_CONNECTION_STRING:
        raise ValueError("missing MONGO_DB_CONNECTION_STRING")
    if not MONGO_BLOK_DATABASE:
        raise ValueError("missing MONGO_DATABASE env")

    return client[MONGO_BLOK_DATABASE]
