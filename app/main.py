from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

import joblib
from app.config import settings
from app.logging_config import logger
import uuid
import time

from app.routers.v1 import router
from app.routers.v2 import router as v2_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model = joblib.load(settings.MODEL_PATH)
    logger.info("ML model loaded successfully")
    yield


app = FastAPI(
    title=settings.API_TITLE,
    lifespan=lifespan
)

Instrumentator().instrument(app).expose(app)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)
app.include_router(v2_router)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    logger.info(
        f"request_id={request_id} | "
        f"method={request.method} | "
        f"path={request.url.path} | "
        f"duration={duration:.4f}s"
    )

    return response


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={
            "detail": "Invalid value provided"
        }
    )


@app.get("/")
def root():
    return {"message": "ml api is alive"}