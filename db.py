from pymongo import MongoClient
import os
from dotenv import load_dotenv
import json

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["ocr_docs"]
collection = db["files"]

def save_file(filename, content, process_time=None, other_info=None):
    doc = {
        "filename": filename,
        "content": content,
        "process_time": process_time or "N/A",  # Default to "N/A" if not provided
        "other_info": other_info or "N/A"       # Default to "N/A" if not provided
    }
    collection.insert_one(doc)

def get_all_files():
    # Retrieve documents with non-empty content and non-empty filenames
    return list(collection.find({"content": {"$ne": ""}, "filename": {"$ne": ""}}, {"_id": 0}))

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
