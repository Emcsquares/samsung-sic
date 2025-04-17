from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print("MongoDB connection successful!")

    db = client["ocr_docs"]
    collection = db["files"]

    files = list(collection.find())
    print(f"Retrieved {len(files)} files:")
    for file in files:
        print(file)

except Exception as e:
    print(f"MongoDB connection failed: {e}")
