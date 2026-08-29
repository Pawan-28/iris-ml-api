# Iris Flower Classification API

## Project Overview

This project is a machine learning REST API that predicts the species of an Iris flower based on its physical measurements.

The API will accept four input features: sepal length, sepal width, petal length, and petal width. A machine learning classification model will process these inputs and return the predicted Iris flower species.

The main goal of this project is to understand how a trained machine learning model can be served through a REST API and gradually developed into a production-ready service.

## Problem Statement

The problem is to classify an Iris flower into one of three species based on its physical measurements:

- Setosa
- Versicolor
- Virginica

This is a classification problem.

## Dataset

The project uses the built-in Iris dataset provided by scikit-learn.

The dataset contains four input features:

- Sepal length
- Sepal width
- Petal length
- Petal width

The target variable represents the Iris flower species.

## Machine Learning Model

The project uses a `RandomForestClassifier` from scikit-learn.

The model is trained using the Iris dataset and evaluated using a test dataset.

The trained model is saved using `joblib` so that it can be loaded later by the FastAPI application without retraining.

### Model Performance

The current model achieved:

```text
Test Accuracy: 90%
```

The exact accuracy may vary depending on the train/test split and model configuration.

## API Contract

### Endpoint

```text
POST /predict
```

### Input

The `/predict` endpoint accepts four numerical features representing the physical measurements of an Iris flower:

- `sepal_length`
- `sepal_width`
- `petal_length`
- `petal_width`

Example request:

```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

### Output

The API returns the predicted Iris flower species along with the prediction confidence, model version, and a unique request ID.

Example response:

```json
{
  "prediction": "setosa",
  "confidence": 0.48,
  "model_version": "1.0",
  "request_id": "unique-request-id"
}
```

## Request Flow

The planned API request flow is:

```text
Client
  ↓
Request Middleware (Request ID + Logging)
  ↓
POST /predict
  ↓
Input Validation
  ↓
Preprocessing Pipeline
  ↓
Machine Learning Model
  ↓
Prediction
  ↓
JSON Response
```

### Flow Explanation

1. The client sends Iris flower measurements to the `/predict` endpoint.
2. The API validates the input data.
3. The same preprocessing used during model training is applied.
4. The processed data is passed to the trained machine learning model.
5. The model predicts the Iris flower species.
6. The API returns the prediction as a JSON response.

## Model Saving

The trained model is saved at:

```text
ml/saved_model/model.joblib
```

The saved model can be loaded later without retraining.

A separate prediction script is used to verify that the saved model can be successfully loaded and used for prediction.

## Project Structure

```text
iris-ml-api/
│
├── app/
│   ├── main.py
│   ├── logging_config.py
│   ├── models/
│   │   └── schemas.py
│   └── routers/
│
├── logs/
│   └── app.log
│
│
├── ml/
│   ├── train.py
│   ├── predict.py
│   └── saved_model/
│       └── model.joblib
│
├── tests/
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Technologies

- Python
- scikit-learn
- FastAPI
- Pydantic
- Uvicorn
- Pandas
- Joblib
- Git
- GitHub

## Current Progress

- [x] Project problem and dataset selected
- [x] API input/output contract planned
- [x] Project architecture planned
- [x] GitHub repository created
- [x] Python virtual environment configured
- [x] Project folder structure created
- [x] Dependencies installed
- [x] `requirements.txt` created
- [x] `.gitignore` configured
- [x] RandomForestClassifier trained
- [x] Model evaluated
- [x] Model saved as `model.joblib`
- [x] Saved model loaded and tested with a prediction
- [x] Basic FastAPI application created
- [x] `GET /` endpoint created
- [x] `POST /predict` endpoint created
- [x] FastAPI Swagger documentation tested
- [x] Pydantic input validation added
- [x] Real ML model integrated with FastAPI
- [x] Model loaded using FastAPI lifespan
- [x] Health check endpoint added
- [x] Error handling implemented
- [x] Custom exception handling added
- [x] Structured logging configured
- [x] Request middleware added
- [x] Unique request IDs implemented
- [x] Prediction success and failure logging added
- [x] Rotating file logging implemented

## Future Development

The project will be developed further by adding:

- Automated testing
- API monitoring and metrics
- Docker containerization
- Deployment
- API versioning

## API Documentation

FastAPI provides automatic interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```