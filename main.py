from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from datetime import datetime

app = FastAPI()

@app.post("/lux")
async def receive_lux_data(request: Request):
    data = await request.json()
    timestamp = datetime.utcnow().isoformat()
    print(f"[{timestamp}] Received data: {data}")

    return JSONResponse(content={"status": "success", "received": data})
