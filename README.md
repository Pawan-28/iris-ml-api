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

### V1 Endpoint

```text
POST /api/v1/predict
```

### V2 Endpoint

```text
POST /api/v2/predict
```

### Input

The `/api/v1/predict` and `/api/v2/predict` endpoints accept four numerical features representing the physical measurements of an Iris flower:

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
  "confidence": 100.0,
  "model_version": "1.0",
  "request_id": "unique-request-id"
}
```

### V2 Output

The V2 API returns the predicted species along with the full probability distribution for all Iris classes, model version, and request ID.

Example response:

```json
{
  "prediction": "setosa",
  "probabilities": {
    "setosa": 1.0,
    "versicolor": 0.0,
    "virginica": 0.0
  },
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
POST /api/v1/predict
or
POST /api/v2/predict
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

1. The client sends Iris flower measurements to the `/api/v1/predict` or `/api/v2/predict` endpoint.
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
│   ├── config.py
│   ├── logging_config.py
│   ├── models/
│   │   └── schemas.py
│   └── routers/
│       ├── v1.py
│       └── v2.py
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
│   ├── conftest.py
│   ├── test_health.py
│   ├── test_predict.py
│   ├── test_batch.py
│   └── test_v2.py
│
├── .dockerignore
├── .env
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
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
- Docker
- Docker Compose

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
- [x] `POST /api/v1/predict` endpoint created
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
- [x] API versioning implemented with `/api/v1` and `/api/v2`
- [x] Batch prediction endpoint added
- [x] Model information endpoint added
- [x] Environment-based configuration added
- [x] `.env` and `.env.example` added
- [x] Automated API tests added with pytest
- [x] Input validation and edge-case tests added
- [x] API v2 endpoint added
- [x] V1 and V2 response shapes tested
- [x] 7 automated tests passing


## Docker

The API is containerized using Docker, allowing the complete application,
including its dependencies and trained machine learning model, to run inside
a portable container.

### Dockerfile

The Dockerfile:

- Uses Python 3.12 Slim as the base image
- Sets `/app` as the working directory
- Installs all project dependencies from `requirements.txt`
- Copies the application code and ML model into the container
- Exposes port `8000`
- Runs the FastAPI application using Uvicorn

The API uses `0.0.0.0` inside Docker so that the application is accessible
from outside the container through the mapped host port.

### Why `0.0.0.0` is used inside Docker

Inside a Docker container, `127.0.0.1` only makes the application accessible
from within the container itself.

Using `0.0.0.0` makes Uvicorn listen on all available network interfaces,
allowing Docker port mapping to expose the API to the host machine.

### Build the Docker Image

```bash
docker build -t ml-api:v1 .
```

### Run the Docker Container

```bash
docker run -p 8000:8000 ml-api:v1
```

### Run with Docker Compose

```bash
docker compose up --build
```

## Future Development

The project will be developed further by adding:

- API monitoring and metrics
- Deployment
- Further API version improvements


## Task 14 — API Versioning and Self-Assessment

### API Versioning

The API now supports multiple versions:

- `POST /api/v1/predict` — returns prediction, confidence, model version, and request ID.
- `POST /api/v2/predict` — returns prediction, full probability distribution, model version, and request ID.

Version 2 introduces a deliberately different response shape while keeping version 1 unchanged.

### Self-Assessment

#### 1. If a client was depending on v1's exact response shape, would anything break?

No. The v1 response shape remains unchanged. The breaking change was introduced through a separate `/api/v2/predict` endpoint. Automated tests verify that both versions work with the same input while returning different response shapes.

#### 2. Where did you have to duplicate code between v1 and v2, and could any of it be shared instead?

Some feature preparation, model prediction, and class mapping logic is duplicated between v1 and v2. In the future, the common prediction logic could be moved into a shared service or helper function, while keeping separate response schemas for each API version.

#### 3. How would you tell your team it's time to deprecate v1 someday?

I would consider deprecating v1 when most clients have migrated to v2, v1 traffic has consistently become very low, and existing v1 users have been informed and given a clear migration path.


## API Documentation

FastAPI provides automatic interactive API documentation at:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)