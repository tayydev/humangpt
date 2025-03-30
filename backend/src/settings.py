import os

from pymongo import MongoClient

username = os.environ.get("MONGO_USER", "username")
password = os.environ.get("MONGO_PASS", "password123")
host = os.environ.get("MONGO_HOST", "localhost")

def get_mongodb_connection():
    connection_string = f"mongodb://{username}:{password}@{host}:27017/"
    client = MongoClient(connection_string)
    return client["humangpt"]
