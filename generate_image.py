from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from google.cloud import logging
from PIL import Image
import io
import os
import time
import requests
import uuid
from dotenv import load_dotenv

app = FastAPI()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_cloud_logging.json"

client = logging.Client()
logger = client.logger("api_usage_log")

load_dotenv()

GOOGLE_ANALYTICS_MEASUREMENT_ID = os.getenv("GOOGLE_ANALYTICS_MEASUREMENT_ID")
GOOGLE_ANALYTICS_API_SECRET = os.getenv("GOOGLE_ANALYTICS_API_SECRET")
GA_ENDPOINT = f"https://www.google-analytics.com/mp/collect?measurement_id={GOOGLE_ANALYTICS_MEASUREMENT_ID}&api_secret={GOOGLE_ANALYTICS_API_SECRET}"

def send_event_to_google_analytics(request, process_time, status_code):
    client_id = str(uuid.uuid4())
    event_data = {
        "client_id": client_id,
        "events": [
            {
                "name": "api_request",
                "params": {
                    "method": request.method,
                    "url": str(request.url),
                    "status_code": status_code,
                    "process_time": process_time,
                }
            }
        ]
    }

    try:
        response = requests.post(GA_ENDPOINT, json=event_data)
        print(f"Sent event to Google Analytics: {event_data}")
        print(f"Response status code: {response.status_code}")
        print(f"Response text: {response.text}")

        if response.status_code != 204:
            print(f"Failed to log event to Google Analytics: {response.text}")
        else:
            print(f"Event successfully logged to Google Analytics")

    except Exception as err:
        print(f"Error sedning event to Google Analytics: {err}")


@app.middleware("http")
async def log_request(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    log_data = {
        "method": request.method,
        "url": str(request.url),
        "status_code": response.status_code,
        "process_time": f"{process_time:.2f} 秒",
    }
    logger.log_struct(log_data)
    send_event_to_google_analytics(request, process_time, response.status_code)
    return response

MAX_WIDTH = 5500
MAX_HEIGHT = 5500

@app.get("/generate_image")
async def generate_image(width: int, height: int):
    if width<=0 or height<=0:
        raise HTTPException(status_code=400, detail="Height and Width must be positive integers.")
    if width > MAX_WIDTH or height > MAX_HEIGHT:
        raise HTTPException(status_code=400, detail=f"Height and Width must be less than or equal to {MAX_HEIGHT} and {MAX_WIDTH}")

    image = Image.new("RGB", (width, height), (0, 0, 255))

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    return StreamingResponse(buffer, media_type="image/png")