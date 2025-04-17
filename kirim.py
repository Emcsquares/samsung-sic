import os
from pymongo import MongoClient
from dotenv import load_dotenv
import json  # For loading the JSON file

# Load environment variables from .env file
load_dotenv()

# Get values from .env file
mongo_uri = os.getenv("MONGO_URI")
mongo_db_name = os.getenv("MONGO_DB_NAME")
mongo_collection = os.getenv("MONGO_COLLECTION")

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client[mongo_db_name]
collection = db[mongo_collection]

# Verify file existence
if not os.path.exists("output.json"):
    print("output.json file does not exist.")
    exit()

# Load JSON data from the file
with open("output.json", "r", encoding="utf-8") as file:
    try:
        data = json.load(file)  # Load single JSON object
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        exit()

# Insert JSON data into MongoDB
result = collection.insert_one(data)
print("Data inserted with ID:", result.inserted_id)