from fastapi import FastAPI, Query, UploadFile, File, Header, HTTPException
from fastapi.responses import JSONResponse
from app.data_loader import load_data, save_data
from app.parser import parse_pdf_to_data
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")

app = FastAPI(title="Medicine Lookup API", version="1.0")
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search")
def search_medicine(name: str = Query(...)):
    data = load_data()
    results = [entry for entry in data["medicines"] if name.lower() in entry["Generic Name"].lower()]

    if not results:
        return JSONResponse(status_code=404, content={"message": "Medicine not found", "updated_at": data["updated_at"]})

    return {"updated_at": data["updated_at"], "results": results}

@app.get("/status")
def get_status():
    data = load_data()
    return {"message": "Service is live", "updated_at": data["updated_at"]}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...), x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    contents = await file.read()
    temp_pdf_path = f"/tmp/{datetime.now().timestamp()}_{file.filename}"

    with open(temp_pdf_path, "wb") as f:
        f.write(contents)

    try:
        parsed_data = parse_pdf_to_data(temp_pdf_path)
        save_data(parsed_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")

    return {"message": "Data updated successfully", "entries": len(parsed_data)}
