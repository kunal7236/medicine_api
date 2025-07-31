from datetime import datetime
from typing import List, Dict
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")


client = MongoClient(MONGO_URI)
db = client["medicineDB"]
collection = db["medicines"]
meta = db["metadata"]

def sanitize_keys(obj):
    if isinstance(obj, dict):
        return {k.replace('.', '_'): sanitize_keys(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_keys(item) for item in obj]
    else:
        return obj

def load_data() -> Dict:
    updated = meta.find_one({"_id": "medicines_update"})
    updated_at = updated["updated_at"] if updated else None
    medicines = list(collection.find({}, {"_id": 0}))
    return {
        "updated_at": updated_at,
        "medicines": medicines
    }

def save_data(medicines: List[Dict], updated_at: str = None):
    if updated_at is None:
        updated_at = datetime.now().isoformat()
    collection.delete_many({})
    if medicines:
        sanitized_data = [sanitize_keys(entry) for entry in medicines]
        collection.insert_many(sanitized_data)

    meta.update_one(
        {"_id": "medicines_update"},
        {"$set": {"updated_at": updated_at}},
        upsert=True
    )
