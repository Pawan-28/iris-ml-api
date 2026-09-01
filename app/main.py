from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import joblib
from app.config import settings
from app.logging_config import logger
import uuid, time
from app.routers.v1 import router



@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model = joblib.load(settings.MODEL_PATH)
    logger.info("ML model loaded successfully")
    yield

app = FastAPI(
    title=settings.API_TITLE,
    lifespan=lifespan)
app.include_router(router)

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


