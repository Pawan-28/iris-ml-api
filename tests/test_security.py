from app.config import settings

def test_missing_api_key(client):
    response = client.post(
        "/api/v1/predict",
        json={
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2
        }
    )

    assert response.status_code == 401


def test_invalid_api_key(client):
    response = client.post(
        "/api/v1/predict",
        headers={
            "X-API-Key": "wrong-api-key"
        },
        json={
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2
        }
    )

    assert response.status_code == 401


def test_unexpected_extra_field(client):
    response = client.post(
        "/api/v1/predict",
        headers={
            "X-API-Key": settings.API_KEY
        },
        json={
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2,
            "unexpected_field": "hello"
        }
    )

    assert response.status_code == 422