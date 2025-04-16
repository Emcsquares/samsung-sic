from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["ocr_docs"]
collection = db["files"]

def save_file(filename, content):
    doc = {"filename": filename, "content": content}
    collection.insert_one(doc)

def get_all_files():
    return list(collection.find({}, {"_id": 0}))

def download_all_files():
    files = get_all_files()
    return "\n\n".join([f"{f['filename']}:\n{f['content']}" for f in files])
