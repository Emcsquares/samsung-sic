from pymongo import MongoClient
import os
from dotenv import load_dotenv
import json

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

try:
    client = MongoClient(
        MONGO_URI,
        serverSelectionTimeoutMS=5000  # 5-second timeout
    )
    client.admin.command('ping')  # Test connection
    db = client["ocr_docs"]
    collection = db["files"]
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    client = None
    db = None
    collection = None

def save_file(filename, content, process_time=None, other_info="manual"):
    if collection is not None:  # Explicitly check for None
        doc = {
            "filename": filename,
            "content": content,
            "process_time": process_time or "N/A",
            "other_info": other_info  # Default to "manual" for manual files
        }
        collection.insert_one(doc)
    else:
        print("MongoDB connection is not available. File not saved.")

def get_all_files():
    if collection is not None:  # Explicitly check for None
        files = list(collection.find({"content": {"$ne": ""}, "filename": {"$ne": ""}}, {"_id": 0}))
        # Ensure all files have the required keys
        for file in files:
            file.setdefault("filename", "Unknown File")
            file.setdefault("content", "No content available.")
            file.setdefault("process_time", "N/A")
        return files
    else:
        print("MongoDB connection is not available.")
        return []

def download_all_files():
    files = get_all_files()
    all_files_text = []
    for f in files:
        fname = f.get('filename', 'Unknown')
        content = f.get('content', '')
        if fname.endswith('.json'):
            try:
                parsed = json.loads(content)
                content = json.dumps(parsed, indent=2)
            except Exception:
                pass
        all_files_text.append(f"{fname}:\n{content}")
    return "\n\n".join(all_files_text)
