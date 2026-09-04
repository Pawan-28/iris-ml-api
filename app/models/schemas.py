from pydantic import BaseModel, Field
from typing import List

class PredictionInput(BaseModel):
    sepal_length: float = Field(..., gt=0, examples=[5.1], description="sepal length must be positive")
    sepal_width: float  = Field(..., gt=0, examples=[3.5], description="sepal width must be positive")
    petal_length: float = Field(..., gt=0, examples=[1.4], description ="petal length must be positive")
    petal_width: float  = Field(..., gt=0, le=10, examples=[0.2], description="petal width must be positive")


class PredictionOutput(BaseModel):
    prediction:    str
    confidence:    float
    model_version: str
    request_id:    str


class PredictionBatchInput(BaseModel):
    items: List[PredictionInput] = Field(..., min_length=1)

class PredictionBatchOutput(BaseModel):
    items: List[PredictionOutput]    



class PredictionV2Output(BaseModel):
    prediction: str
    probabilities: dict[str, float]
    model_version: str
    request_id: str    