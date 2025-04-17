from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"  # Update if using a remote server
client = MongoClient(MONGO_URI)

try:
    # Check server connection
    client.admin.command('ping')
    print("MongoDB connection successful!")
except Exception as e:
    print(f"MongoDB connection failed: {e}")
