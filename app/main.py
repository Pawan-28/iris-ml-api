from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import joblib
from pathlib import Path
from app.models.schemas import PredictionInput, PredictionOutput
from app.logging_config import logger
import uuid, time

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH =BASE_DIR / 'ml' / 'saved_model' / 'model.joblib'
MODEL_VERSION = "1.0"
model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    model = joblib.load(MODEL_PATH)
    logger.info("ML model loaded successfully")
    yield

app = FastAPI(lifespan=lifespan)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    logger.info(
        f"request_id={request_id} |"
        f"method={request.method} |"
        f"path={request.url.path} |"
        f"duration={duration:.4f}s"
    )

    return response

@app.exception_handler(ValueError)
async def value_error_handler(request:Request, exc:ValueError):
    return JSONResponse(
        status_code=400,
        content={
            "detail": "Invalid value provided"
        }
    )

@app.get("/")
def root():
    return{ "message": "ml api is alive"}

@app.get("/health")
def health():
    return{
        "status": "ok",
        "model_loaded": model is not None
    }

@app.post("/predict",response_model = PredictionOutput)
def predict(data:PredictionInput, request: Request):
    try:
        
        
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
        confidence = round(float(max(probabilities[0])) * 100, 2)
        request_id = request.state.request_id

        logger.info(
            f"Prediction successful | "
            f"request_id={request_id} | "
            f"prediction={predicted_class}"
            )
        return {"prediction": predicted_class,
                "confidence": confidence,
                "model_version": MODEL_VERSION,
                "request_id": request_id
                }
    except Exception as e:
        logger.error(
            f"Prediction Failed | "
            f"request_id={request.state.request_id} | "
            f"error={str(e)}"
        )

        
        raise HTTPException(
            status_code=500,
            detail="Prediction Failed"
        )
    