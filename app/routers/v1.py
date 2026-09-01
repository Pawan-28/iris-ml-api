from fastapi import APIRouter, HTTPException, Request
from app.models.schemas import (
    PredictionInput,
    PredictionOutput,
    PredictionBatchInput,
    PredictionBatchOutput
)
from app.config import settings
from app.logging_config import logger

router = APIRouter(
    prefix="/api/v1",
    tags=["api v1"]

)


@router.get("/health")
def health():
    return{
        "status": "ok",
        "model_loaded": True
    }

@router.post("/predict", response_model=PredictionOutput)
def predict(data: PredictionInput, request: Request):
    try:
        features =[[
            data.sepal_length,
            data.sepal_width,
            data.petal_length,
            data.petal_width
        ]]

        model = request.app.state.model

        prediction = model.predict(features)
        probabilities = model.predict_proba(features)

        class_names = ["setosa", "versicolor", "virginica"]

        predicted_class = class_names[prediction[0]]
        confidence = round(float(max(probabilities[0])) * 100, 2)

        request_id = request.state.request_id
        logger.info(
            f"Prediction successful | "
            f"request_id={request_id} | "
            f"prediction={predicted_class}"

        )

        return {
            "prediction": predicted_class,
            "confidence": confidence,
            "model_version": settings.MODEL_VERSION,
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



@router.post("/predict-batch", response_model=PredictionBatchOutput)
def predict_batch(data:PredictionBatchInput, request: Request):
    try:
        if len(data.items) > settings.MAX_BATCH_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"Batch size can't exceed {settings.MAX_BATCH_SIZE}"
            )
        features = [
            [
                item.sepal_length,
                item.sepal_width,
                item.petal_length,
                item.petal_width
            ]
            for item in data.items
        ]

        model = request.app.state.model

        predictions = model.predict(features)
        probabilities = model.predict_proba(features)

        class_names = ["setosa", "versicolor", "virginica"]

        results = []

        for prediction, probability in zip(predictions, probabilities):
            predicted_class = class_names[prediction]
            confidence = round(float(max(probability))* 100, 2)

            results.append(
                PredictionOutput(
                    prediction=predicted_class,
                    confidence=confidence,
                    model_version=settings.MODEL_VERSION,
                    request_id=request.state.request_id

                )
            )

        logger.info(
            f"Batch prediction successful | "
            f"request_id={request.state.request_id} | "
            f"batch_size={len(data.items)}"
        )

        return {
            "items": results
        }    
    except Exception as e:
        logger.error(
            f"Batch prediction failed | "
            f"request_id={request.state.request_id} | "
            f"batch_size={len(data.items)} | "
            f"error={str(e)}"
        )

        raise HTTPException(
            status_code = 500,
            detail="Batch prediction failed"
        )
@router.get("/model-info")
def model_info():
    return{
        "model_type": "RandomForestClassifier",
        "model_version": settings.MODEL_VERSION,
        "training_date": "2026-08-26",
        "features": [
            "sepal_length",
            "sepal_width",
            "petal_length",
            "petal_width"
        ]
    }
# V2 will introduce a breaking change while keeping V1 unchanged.
# For example, V2 may return the full probability distribution
# for all Iris classes instead of only the confidence score.    
