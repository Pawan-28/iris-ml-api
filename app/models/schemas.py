from pydantic import BaseModel, Field

class PredictionInput(BaseModel):
    sepal_length: float = Field(..., gt=0, description="sepal lenght must be postive")
    sepal_width: float  = Field(..., gt=0, description="sepal widht must be postive")
    petal_length: float = Field(..., gt=0, description ="petal_lenght must be postive")
    petal_width: float  = Field(..., gt=0, le=10, description="petal_widht must be postive")

