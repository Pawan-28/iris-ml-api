def test_metrics_endpoint_and_prediction_counter(client, auth_headers):
    payload = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }

    prediction_response = client.post(
        "/api/v1/predict",
        json=payload,
        headers=auth_headers
    )

    assert prediction_response.status_code == 200

    metrics_response = client.get("/metrics")

    assert metrics_response.status_code == 200

    metrics = metrics_response.text

    assert "iris_predictions_total" in metrics
    assert 'predicted_class="setosa"' in metrics