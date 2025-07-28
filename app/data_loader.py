import json
from datetime import datetime
from typing import List, Dict

DATA_FILE = "app/data.json"

def load_data() -> Dict:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(medicines: List[Dict], updated_at: str = None):
    if updated_at is None:
        updated_at = datetime.now().isoformat()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "updated_at": updated_at,
            "medicines": medicines
        }, f, indent=2)
