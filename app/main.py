from contextlib import asynccontextmanager
from fastapi import FastAPI
import joblib
from pathlib import Path
from app.models.schemas import PredictionInput
import uuid

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH =BASE_DIR / 'ml' / 'saved_model' / 'model.joblib'

model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    model = joblib.load(MODEL_PATH)
    print("ml model load successfully")
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return{ "message": "ml api is alive"}

@app.get("/health")
def health():
    return{
        "status": "ok",
        "model_loaded": model is not None
    }

@app.post("/predict")
def predict(data:PredictionInput):

    features = [[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width
    ]]

    prediction = model.predict(features) 
    probabilities = model.predict_proba(features)

    class_name = ['setosa', 'versicolor', 'virginica']

    predicted_class = class_name[prediction[0]]
    confidence = float(max(probabilities[0]))

    request_id = str(uuid.uuid4())
    return {"prediction": predicted_class,
            "confidence": confidence,
            "request_id": request_id
            }
# app = FastAPI()


# @app.get("/")
# def root():
#     return {"message": "ML API is alive"}


# @app.post("/predict")
# def predict():
#     return {"prediction": "hardcoded_result"}