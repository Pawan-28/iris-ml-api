from fastapi import APIRouter, HTTPException, Request

from app.models.schemas import PredictionInput, PredictionV2Output
from app.config import settings
from app.logging_config import logger


router = APIRouter(
    prefix="/api/v2",
    tags=["api v2"]
)


@router.post("/predict", response_model=PredictionV2Output)
def predict_v2(data: PredictionInput, request: Request):
    try:
        features = [[
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

        probability_distribution = {
            class_name: round(float(probability), 4)
            for class_name, probability in zip(
                class_names,
                probabilities[0]
            )
        }

        request_id = request.state.request_id

        logger.info(
            f"V2 prediction successful | "
            f"request_id={request_id} | "
            f"prediction={predicted_class}"
        )

        return {
            "prediction": predicted_class,
            "probabilities": probability_distribution,
            "model_version": settings.MODEL_VERSION,
            "request_id": request_id
        }

    except Exception as e:
        logger.error(
            f"V2 prediction failed | "
            f"request_id={request.state.request_id} | "
            f"error={str(e)}"
        )

        raise HTTPException(
            status_code=500,
            detail="V2 Prediction Failed"
        )