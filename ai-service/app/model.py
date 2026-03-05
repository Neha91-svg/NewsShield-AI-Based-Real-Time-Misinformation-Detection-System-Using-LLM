from transformers import pipeline

classifier = pipeline(
    "text-classification",
    model="mrm8488/bert-tiny-finetuned-fake-news-detection"
)

def predict_news(text: str):
    result = classifier(text)[0]
    return {
        "prediction": "FAKE" if result["label"] == "LABEL_0" else "REAL",
        "confidence": round(result["score"] * 100, 2)
    }