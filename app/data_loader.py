#import json
from datetime import datetime
from typing import List, Dict
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
#DATA_FILE = "app/data.json"

client = MongoClient(MONGO_URI)
db = client["medicineDB"]
collection = db["medicines"]
meta = db["metadata"]

def load_data() -> Dict:
    # with open(DATA_FILE, "r", encoding="utf-8") as f:
    #     return json.load(f)
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
    # with open(DATA_FILE, "w", encoding="utf-8") as f:
    #     json.dump({
    #         "updated_at": updated_at,
    #         "medicines": medicines
    #     }, f, indent=2)
    collection.delete_many({})
    if medicines:
        collection.insert_many(medicines)

    meta.update_one(
        {"_id": "medicines_update"},
        {"$set": {"updated_at": updated_at}},
        upsert=True
    )
