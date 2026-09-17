# Testing Documentation

## 1. Testing Environment

- Application: Iris ML Classification API
- Framework: FastAPI
- Containerization: Docker + Docker Compose
- Base URL: `http://127.0.0.1:8000`
- Test environment: Local Docker container
- Model: RandomForestClassifier

---

## 2. Integration Testing

Integration tests were performed against the running Docker container using HTTP requests.

### Health Check

Endpoint:

`GET /api/v1/health`

Result:

```json
{
  "status": "ok",
  "model_loaded": true
}
```

Status: **PASS**

---

### Single Prediction

Endpoint:

`POST /api/v1/predict`

A valid Iris flower input was submitted with API authentication.

Result:

```json
{
  "prediction": "setosa",
  "confidence": 100.0,
  "model_version": "1.0"
}
```

Status: **PASS**

---

### Batch Prediction

Endpoint:

`POST /api/v1/predict-batch`

Two Iris flower samples were submitted in a single request.

Predictions returned:

- setosa
- virginica

Status: **PASS**

---

### Metrics Endpoint

Endpoint:

`GET /metrics`

The endpoint returned valid Prometheus-format metrics.

Verified metrics included:

- `iris_predictions_total`
- `http_requests_total`
- HTTP request latency metrics

Status: **PASS**

---

## 3. Load Testing

A basic concurrent load test was performed against:

`POST /api/v1/predict`

### Test Configuration

- Total requests: 100
- Concurrent background requests: 100
- Request type: Single prediction
- Authentication: API key
- Target: Running Docker container

### Result

Prometheus metrics recorded:

```text
http_requests_total{handler="/api/v1/predict",method="POST",status="2xx"} 101.0
```

The prediction metrics also recorded successful predictions:

```text
iris_predictions_total{predicted_class="setosa"} 102.0
iris_predictions_total{predicted_class="virginica"} 1.0
```

The API successfully processed the load-test requests without recorded HTTP 5xx failures.

Status: **PASS**

---

## 4. Automated Tests

Automated tests were executed inside the Docker container using:

```bash
docker exec -it iris-ml-api pytest
```

Final result:

```text
11 passed, 4445 warnings in 2.33s
```

The test suite covered:

- Batch prediction
- Health endpoint
- Prometheus metrics
- Single prediction
- API security
- V2 API

Status: **PASS**

---

## 5. Issue Found During Testing

### Issue

Running `pytest` inside the Docker container initially resulted in:

```text
ModuleNotFoundError: No module named 'app'
```

The tests worked when explicitly setting:

```bash
PYTHONPATH=/app pytest
```

### Root Cause

The Docker environment did not explicitly define `/app` as the Python module search path.

### Fix

The Dockerfile was updated with:

```dockerfile
ENV PYTHONPATH=/app
```

### Verification

After updating the Dockerfile, the Docker image was rebuilt and the container was restarted:

```bash
docker compose build
docker compose up -d
```

The test suite was then executed again:

```bash
docker exec -it iris-ml-api pytest
```

All tests passed successfully:

```text
11 passed, 4445 warnings in 2.33s
```

Status: **FIXED AND VERIFIED**

---

## 6. Final Testing Summary

| Test | Result |
|---|---|
| Health endpoint | PASS |
| Single prediction | PASS |
| Batch prediction | PASS |
| Metrics endpoint | PASS |
| Concurrent load test | PASS |
| Automated tests | PASS |
| Docker pytest import issue | FIXED |
| Final Docker test suite | 11 PASSED |

The Iris ML API was successfully tested against the running Docker environment, monitored using Prometheus metrics, and verified with automated tests.

The Docker pytest import issue was identified during testing, fixed by explicitly setting the Python module path, and verified with the complete test suite.