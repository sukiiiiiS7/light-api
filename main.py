from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
import os

app = FastAPI()

# Load environment variables from .env file
load_dotenv()   
MONGO_URI = os.getenv("MONGO_URI")

# Connect to MongoDB Atlas database
client = MongoClient(MONGO_URI)
db = client["plant_data"]  # Database name
db_collection = db["light_data"]  # Collection name for light data

@app.get("/")
def root():
    return {
        "message": "🌞 Light API with MongoDB is running.",
        "endpoints": [
            "/lux (POST) - Send lux value",
            "/lux (GET) - Get all recorded lux values from MongoDB"
        ]
    }

@app.post("/lux")
async def receive_lux(request: Request):
    data = await request.json()
    lux = data.get("lux")

    if lux is None:
        return {"status": "error", "message": "Missing 'lux' field"}

    timestamp = datetime.utcnow().replace(microsecond=0).isoformat()

    # Save to MongoDB
    db_collection.insert_one({
        "lux": lux,
        "timestamp": timestamp
    })

    # Return only serializable data
    return {
        "status": "success",
        "saved": {
            "lux": lux,
            "timestamp": timestamp
        }
    }


@app.get("/lux")
def get_lux_records():
    try:
        # Retrieve all records and exclude MongoDB's internal _id field
        records = list(db_collection.find({}, {"_id": 0}))
        return JSONResponse(content=records)
    except Exception as e:
        return {"error": str(e)}
