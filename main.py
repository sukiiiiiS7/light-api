from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from datetime import datetime
import json
import os

app = FastAPI()

DATA_FILE = "lux_records.json"

# Create file if it doesn't exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

@app.get("/")
def root():
    return {
        "message": "🌞 Light API is running.",
        "endpoints": [
            "/lux (POST) - Send lux value",
            "/lux (GET) - Get all recorded lux values"
        ]
    }

@app.post("/lux")
async def receive_lux(request: Request):
    data = await request.json()
    lux = data.get("lux")

    if lux is None:
        return {"status": "error", "message": "Missing 'lux' field"}

    record = {
        "lux": lux,
        "timestamp": datetime.utcnow().isoformat()
    }

    with open(DATA_FILE, "r+") as f:
        try:
            records = json.load(f)
        except json.JSONDecodeError:
            records = []
        records.append(record)
        f.seek(0)
        json.dump(records, f, indent=2)

    return {"status": "success", "received": record}

@app.get("/lux")
def get_lux_records():
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        return JSONResponse(content=data)
    except Exception as e:
        return {"error": str(e)}
