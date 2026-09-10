def test_v1_and_v2_have_different_response_shapes(client, auth_headers):
    payload = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }

    v1_response = client.post(
        "/api/v1/predict",
        json=payload,
        headers=auth_headers
    )

    v2_response = client.post(
        "/api/v2/predict",
        json=payload,
        headers=auth_headers
    )

    assert v1_response.status_code == 200
    assert v2_response.status_code == 200

    v1_data = v1_response.json()
    v2_data = v2_response.json()

    # V1 returns confidence
    assert "confidence" in v1_data
    assert "probabilities" not in v1_data

    # V2 returns full probability distribution
    assert "probabilities" in v2_data
    assert "confidence" not in v2_data

    # Both versions still return the prediction
    assert v1_data["prediction"] in [
        "setosa",
        "versicolor",
        "virginica"
    ]

    assert v2_data["prediction"] in [
        "setosa",
        "versicolor",
        "virginica"
    ]

    # V2 should return all three Iris class probabilities
    assert set(v2_data["probabilities"].keys()) == {
        "setosa",
        "versicolor",
        "virginica"
    }