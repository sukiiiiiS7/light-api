from fastapi import FastAPI, Request
from datetime import datetime
import json

app = FastAPI()

# Local file to store lux readings
DATA_FILE = "lux_records.json"

# Ensure file exists
try:
    with open(DATA_FILE, "x") as f:
        json.dump([], f)
except FileExistsError:
    pass

@app.post("/lux")
async def receive_lux(request: Request):
    data = await request.json()
    lux = data.get("lux")

    if lux is None:
        return {"status": "error", "msg": "Missing 'lux'"}

    # Record with timestamp
    record = {
        "lux": lux,
        "timestamp": datetime.utcnow().isoformat()
    }

    # Append to file
    with open(DATA_FILE, "r+") as f:
        records = json.load(f)
        records.append(record)
        f.seek(0)
        json.dump(records, f, indent=2)

    return {"status": "ok", "received": record}
