from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import NewsRequest
from app.model import predict_news
from app.video import video_to_text
import os
import uuid

app = FastAPI()

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # production me specific URL dena
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TEXT PREDICTION
@app.post("/predict")
def predict(news: NewsRequest):
    if not news.text.strip():
        raise HTTPException(status_code=400, detail="Text is empty")
    return predict_news(news.text)


# VIDEO PREDICTION
@app.post("/predict-video")
async def predict_video(file: UploadFile = File(...)):
    temp_path = f"temp_{uuid.uuid4().hex}_{file.filename}"

    try:
        with open(temp_path, "wb") as buffer:
            buffer.write(await file.read())

        extracted_text = video_to_text(temp_path)

        if not extracted_text:
            raise HTTPException(
                status_code=400,
                detail="No speech detected in video"
            )

        result = predict_news(extracted_text)

        return {
            "extracted_text": extracted_text,
            "prediction": result["prediction"],
            "confidence": result["confidence"]
        }

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)