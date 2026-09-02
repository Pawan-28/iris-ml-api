def test_predict_batch_oversized(client):
    items = []

    for _ in range(101):
        items.append({
            "sepal_length": 5.1,
            "sepal_width": 3.5,
            "petal_length": 1.4,
            "petal_width": 0.2
        })

    response = client.post(
        "/api/v1/predict-batch",
        json={"items": items}
    )

    assert response.status_code == 400



def test_model_info(client):
    response = client.get("/api/v1/model-info")

    assert response.status_code == 200

    data = response.json()

    assert "model_type" in data
    assert "model_version" in data
    assert "training_date" in data
    assert "features" in data