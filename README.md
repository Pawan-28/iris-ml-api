# Iris Flower Classification API

## Project Overview

This project is a machine learning REST API that predicts the species of an Iris flower based on its physical measurements.

The API accepts four input features:

- Sepal length
- Sepal width
- Petal length
- Petal width

A trained machine learning classification model processes these inputs and returns the predicted Iris flower species.

The main goal of this project is to understand how a trained machine learning model can be served through a REST API and gradually developed into a production-ready service.

---

## Problem Statement

The problem is to classify an Iris flower into one of three species based on its physical measurements:

- Setosa
- Versicolor
- Virginica

This is a supervised machine learning classification problem.

---

## Dataset

The project uses the built-in Iris dataset provided by scikit-learn.

The dataset contains four input features:

- Sepal length
- Sepal width
- Petal length
- Petal width

The target variable represents the Iris flower species.

---

## Machine Learning Model

The project uses a `RandomForestClassifier` from scikit-learn.

The model is trained using the Iris dataset and evaluated using a test dataset.

The training process uses:

- Train/test split
- Stratified sampling
- StandardScaler
- RandomForestClassifier
- Accuracy evaluation

The trained model and preprocessing pipeline are saved using `joblib`.

The saved model can then be loaded by the FastAPI application without retraining.

### Model Performance

The current model achieved:

```text
Test Accuracy: 90%
```

The exact accuracy may vary depending on the train/test split and model configuration.

---

## API Contract

### V1 Endpoint

```text
POST /api/v1/predict
```

The V1 endpoint returns:

- Prediction
- Confidence
- Model version
- Request ID

### V2 Endpoint

```text
POST /api/v2/predict
```

The V2 endpoint returns:

- Prediction
- Full probability distribution
- Model version
- Request ID

---

## Input

The `/api/v1/predict` and `/api/v2/predict` endpoints accept four numerical features representing the physical measurements of an Iris flower.

```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

Input validation is implemented using Pydantic.

Invalid values such as negative measurements, missing fields, or unexpected fields are rejected by the API.

---

## V1 Output

Example:

```json
{
  "prediction": "setosa",
  "confidence": 100.0,
  "model_version": "1.0",
  "request_id": "unique-request-id"
}
```

---

## V2 Output

Version 2 provides the complete probability distribution for all Iris classes.

Example:

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

Version 2 intentionally uses a different response structure while keeping V1 unchanged.

---

## API Security

Prediction and model information endpoints are protected using API key authentication.

The API key must be provided using the following HTTP header:

```text
X-API-Key: your-secret-api-key
```

### Protected Endpoints

- `POST /api/v1/predict`
- `POST /api/v1/predict-batch`
- `GET /api/v1/model-info`
- `POST /api/v2/predict`

Requests with a missing or invalid API key return:

```json
{
  "detail": "Invalid or missing API key"
}
```

The API key is stored using environment variables and is not hardcoded into the application.

---

## Request Flow

The API request flow is:

```text
Client
  |
  v
Request Middleware
(Request ID + Logging)
  |
  v
API Router
  |
  +--------------------+
  |                    |
  v                    v
V1 Endpoint          V2 Endpoint
  |                    |
  +---------+----------+
            |
            v
     Pydantic Validation
            |
            v
   Feature Preparation
            |
            v
   Saved ML Pipeline
            |
            v
       Prediction
            |
            v
     JSON Response
```

### Flow Explanation

1. The client sends Iris flower measurements to the API.
2. Request middleware generates a unique request ID and records request information.
3. Pydantic validates the input data.
4. The application prepares the four model features.
5. The saved machine learning pipeline processes the input.
6. The model predicts the Iris flower species.
7. Prometheus prediction metrics are updated.
8. The API returns the prediction as a JSON response.

---

## Model Saving

The trained model is saved at:

```text
ml/saved_model/model.joblib
```

The saved model contains the trained machine learning pipeline.

A separate prediction script is available at:

```text
ml/predict.py
```

This script verifies that the saved model can be loaded and used for prediction without retraining.

---

## Project Structure

```text
iris-ml-api/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── logging_config.py
│   ├── metrics.py
│   ├── security.py
│   │
│   ├── models/
│   │   └── schemas.py
│   │
│   └── routers/
│       ├── v1.py
│       └── v2.py
│
├── tests/
│   ├── conftest.py
│   ├── test_health.py
│   ├── test_predict.py
│   ├── test_batch.py
│   ├── test_metrics.py
│   ├── test_v2.py
│   └── test_security.py
│
├── logs/
│   └── app.log
│
├── ml/
│   ├── train.py
│   ├── predict.py
│   └── saved_model/
│       └── model.joblib
│
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── TESTING.md
```

---

## API Endpoints

| Method | Endpoint | Authentication | Description |
|---|---|---|---|
| GET | `/` | No | API status |
| GET | `/api/v1/health` | No | Health check |
| POST | `/api/v1/predict` | X-API-Key | Single prediction |
| POST | `/api/v1/predict-batch` | X-API-Key | Batch prediction |
| GET | `/api/v1/model-info` | X-API-Key | Model information |
| POST | `/api/v2/predict` | X-API-Key | Prediction with probability distribution |
| GET | `/metrics` | No | Prometheus metrics |

---

## API Usage

The examples below use the local Docker API:

```text
http://127.0.0.1:8000
```

Replace `your-secret-api-key` with the API key configured in your environment.

### 1. Root

```bash
curl http://127.0.0.1:8000/
```

Example response:

```json
{
  "message": "ml api is alive"
}
```

---

### 2. Health Check

```bash
curl http://127.0.0.1:8000/api/v1/health
```

Example response:

```json
{
  "status": "ok",
  "model_loaded": true
}
```

---

### 3. V1 Single Prediction

```bash
curl -X POST http://127.0.0.1:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-api-key" \
  -d '{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
  }'
```

Example response:

```json
{
  "prediction": "setosa",
  "confidence": 100.0,
  "model_version": "1.0",
  "request_id": "unique-request-id"
}
```

---

### 4. Batch Prediction

```bash
curl -X POST http://127.0.0.1:8000/api/v1/predict-batch \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-api-key" \
  -d '{
    "items": [
      {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
      },
      {
        "sepal_length": 6.0,
        "sepal_width": 3.0,
        "petal_length": 4.8,
        "petal_width": 1.8
      }
    ]
  }'
```

The endpoint processes multiple samples in a single request.

---

### 5. Model Information

```bash
curl http://127.0.0.1:8000/api/v1/model-info \
  -H "X-API-Key: your-secret-api-key"
```

Example response:

```json
{
  "model_type": "RandomForestClassifier",
  "model_version": "1.0",
  "training_date": "2026-08-26",
  "features": [
    "sepal_length",
    "sepal_width",
    "petal_length",
    "petal_width"
  ]
}
```

---

### 6. V2 Prediction

```bash
curl -X POST http://127.0.0.1:8000/api/v2/predict \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-api-key" \
  -d '{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
  }'
```

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

---

### 7. Prometheus Metrics

```bash
curl http://127.0.0.1:8000/metrics
```

The endpoint exposes Prometheus-compatible metrics including:

- HTTP request metrics
- HTTP request latency metrics
- `iris_predictions_total`

The custom prediction metric tracks predictions by predicted class.

---

## Monitoring and Metrics

Prometheus instrumentation is implemented using:

```text
prometheus-fastapi-instrumentator
```

The metrics endpoint is:

```text
GET /metrics
```

A custom metric is also implemented:

```text
iris_predictions_total
```

The metric uses the predicted class as a label:

```text
iris_predictions_total{predicted_class="setosa"}
```

This provides basic monitoring of model prediction activity.

---

## Logging

Structured application logging is implemented using Python's logging module.

The application provides:

- Console logging
- Rotating file logging
- Request IDs
- HTTP method logging
- Request path logging
- Request duration logging
- Prediction success logging
- Prediction failure logging
- Batch size logging

Application logs are stored in:

```text
logs/app.log
```

Log files use rotation with a maximum size of 5 MB and up to 3 backup files.

---

## Configuration

Application configuration is managed using `pydantic-settings`.

Configuration values are stored in environment variables.

Example `.env` configuration:

```env
MODEL_PATH=ml/saved_model/model.joblib
MODEL_VERSION=1.0
LOG_LEVEL=INFO
MAX_BATCH_SIZE=100
API_TITLE=Iris Flower Classification API
API_KEY=your-secret-api-key
ALLOWED_ORIGINS=http://localhost:3000
```

The `.env` file should not be committed to Git.

Use `.env.example` as the template for required configuration.

---

## CORS

CORS is configured using FastAPI's `CORSMiddleware`.

Allowed origins are configured through:

```env
ALLOWED_ORIGINS=http://localhost:3000
```

This avoids hardcoding deployment-specific origins directly into the application.

---

## Technologies

- Python
- scikit-learn
- FastAPI
- Pydantic
- Pydantic Settings
- Uvicorn
- Pandas
- NumPy
- Joblib
- Prometheus
- Git
- GitHub
- GitHub Actions
- Docker
- Docker Compose
- Pytest

---

## Docker

The API is containerized using Docker.

The container includes:

- Python runtime
- Application code
- API dependencies
- Trained machine learning model

### Dockerfile

The Dockerfile:

- Uses Python 3.12 Slim as the base image
- Sets `/app` as the working directory
- Installs dependencies from `requirements.txt`
- Copies the application and ML model
- Exposes port `8000`
- Runs FastAPI using Uvicorn

The application listens on:

```text
0.0.0.0:8000
```

### Why `0.0.0.0` is used

Inside a Docker container, `127.0.0.1` only makes the application accessible from inside the container.

Using `0.0.0.0` allows Uvicorn to listen on all network interfaces so Docker port mapping can expose the API to the host machine.

---

## Build the Docker Image

```bash
docker build -t ml-api:v1 .
```

---

## Run the Docker Container

```bash
docker run -p 8000:8000 ml-api:v1
```

---

## Run with Docker Compose

```bash
docker compose up --build
```

To run the application in the background:

```bash
docker compose up --build -d
```

To stop the application:

```bash
docker compose down
```

---

## Testing

The project includes automated testing, integration testing, Docker testing, and concurrent load testing.

### Automated Tests

The final automated test suite contains:

```text
11 passed
```

Tests cover:

- Health endpoint
- Single prediction
- Input validation
- Missing fields
- Batch prediction
- Model information
- API security
- Missing API key
- Invalid API key
- Unexpected request fields
- Prometheus metrics
- V1/V2 response differences

Run tests locally:

```bash
python -m pytest -v
```

Run tests inside Docker:

```bash
docker exec -it iris-ml-api pytest
```

Final Docker test result:

```text
11 passed
```

---

## Integration Testing

Integration testing was performed against the running Docker container using HTTP requests.

The following endpoints were verified:

```text
GET  /api/v1/health
POST /api/v1/predict
POST /api/v1/predict-batch
GET  /metrics
```

All tested endpoints returned successful responses.

Detailed integration testing results are documented in:

```text
TESTING.md
```

---

## Load Testing

A concurrent load test was performed against:

```text
POST /api/v1/predict
```

Test configuration:

```text
Total requests: 100
Concurrent requests: 100
Authentication: API key
Target: Running Docker container
```

The API successfully processed the load test without recorded HTTP 5xx failures.

---

## Bug Fix During Testing

During Docker testing, pytest initially produced:

```text
ModuleNotFoundError: No module named 'app'
```

The issue occurred because the Docker environment did not explicitly define the application directory as the Python module search path.

The Dockerfile was updated with:

```dockerfile
ENV PYTHONPATH=/app
```

After rebuilding the Docker image and restarting the container, the complete test suite passed:

```text
11 passed
```

The issue and verification steps are documented in:

```text
TESTING.md
```

---

## Current Progress

### Phase 1

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
- [x] Saved model loaded and tested
- [x] Basic FastAPI application created

### Phase 2

- [x] Pydantic input validation
- [x] Real ML model integrated
- [x] Model loaded using FastAPI lifespan
- [x] Health check endpoint
- [x] Error handling
- [x] Custom exception handling
- [x] Structured logging
- [x] Request middleware
- [x] Unique request IDs
- [x] Prediction logging
- [x] Rotating file logging

### Phase 3

- [x] API versioning with `/api/v1` and `/api/v2`
- [x] Batch prediction endpoint
- [x] Model information endpoint
- [x] Environment-based configuration
- [x] `.env.example`
- [x] Automated pytest suite
- [x] V1/V2 response shape testing

### Phase 4

- [x] Docker containerization
- [x] Docker Compose
- [x] API key authentication
- [x] CORS configuration
- [x] Input edge-case handling
- [x] Security tests

### Phase 5

- [x] Prometheus metrics
- [x] Integration testing
- [x] Concurrent load testing
- [x] Docker testing
- [x] Docker pytest issue identified and fixed
- [x] 11 automated tests passing
- [x] GitHub Actions CI implemented
- [x] GitHub Actions workflow passing
- [ ] Public cloud deployment
- [ ] Final deployed API verification

---

## Independent Extension

### GitHub Actions CI

A GitHub Actions CI workflow was implemented as an independent extension.

The workflow automatically runs the project's pytest test suite when:

- Code is pushed to the `main` branch
- A pull request targets the `main` branch

### CI Pipeline

The workflow performs the following steps:

1. Checks out the repository.
2. Sets up Python 3.12.
3. Installs project dependencies.
4. Runs the complete pytest test suite.

The final GitHub Actions workflow completed successfully with:

```text
11 passed
```

This provides automated regression testing and helps ensure that future code changes do not break the existing API functionality.

---

## Deployment

The Dockerized API is intended to be deployed to a cloud hosting platform that supports Docker containers.

### Public API URL

```text
Public API URL:
https://iris-ml-api-xtnf.onrender.com

Swagger Documentation:
https://iris-ml-api-xtnf.onrender.com/docs
```

### Swagger Documentation

```text
TO_BE_UPDATED_AFTER_DEPLOYMENT/docs
```

### Health Check

```text
TO_BE_UPDATED_AFTER_DEPLOYMENT/api/v1/health
```

### Prometheus Metrics

```text
TO_BE_UPDATED_AFTER_DEPLOYMENT/metrics
```

The actual public URLs will be added after deployment and final verification.

---

## API Documentation

FastAPI provides automatic interactive API documentation through Swagger UI.

### Local Documentation

```text
http://127.0.0.1:8000/docs
```

Open:

```text
http://127.0.0.1:8000/docs
```

to test the API interactively.

FastAPI also provides the OpenAPI specification at:

```text
http://127.0.0.1:8000/openapi.json
```

---

## API Versioning

The API supports multiple versions.

### V1

```text
POST /api/v1/predict
```

Returns:

- Prediction
- Confidence
- Model version
- Request ID

### V2

```text
POST /api/v2/predict
```

Returns:

- Prediction
- Full probability distribution
- Model version
- Request ID

Version 2 introduces a deliberately different response shape while keeping version 1 unchanged.

---

## Task 14 — Self-Assessment

### 1. If a client was depending on V1's exact response shape, would anything break?

No.

The V1 response shape remains unchanged.

The breaking change was introduced through a separate `/api/v2/predict` endpoint.

Automated tests verify that both versions work with the same input while returning different response shapes.

### 2. Where did you have to duplicate code between V1 and V2, and could any of it be shared instead?

Some feature preparation, model prediction, and class mapping logic is duplicated between V1 and V2.

In the future, common prediction logic could be moved into a shared service or helper function while keeping separate response schemas for each API version.

### 3. How would you tell your team it is time to deprecate V1 someday?

I would consider deprecating V1 when most clients have migrated to V2, V1 traffic has consistently become very low, and existing V1 users have been informed and provided with a clear migration path.

---

## What I Learned

Through this project, I learned how to:

- Train and save a machine learning classification model.
- Serve a trained ML model using FastAPI.
- Validate API inputs using Pydantic.
- Load a model once using FastAPI lifespan.
- Design versioned APIs using `/api/v1` and `/api/v2`.
- Implement API key authentication.
- Configure applications using environment variables.
- Implement structured logging.
- Generate unique request IDs.
- Add Prometheus monitoring metrics.
- Create batch prediction endpoints.
- Containerize an ML API using Docker.
- Use Docker Compose.
- Write automated tests using pytest.
- Perform integration testing.
- Perform concurrent load testing.
- Identify and fix Docker environment issues.
- Automate testing using GitHub Actions.
- Document and prepare an ML API for deployment.

---

## Future Development

Possible future improvements include:

- Grafana dashboard for advanced monitoring
- Model retraining and automated model versioning
- Response caching for frequently repeated predictions
- Cloud deployment with production monitoring
- Further API performance optimization
- Centralized log management
- CI/CD deployment automation