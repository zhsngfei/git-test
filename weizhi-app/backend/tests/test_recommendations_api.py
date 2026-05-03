from fastapi.testclient import TestClient

from app.main import app


def test_city_recommendations_generate_then_cache() -> None:
    client = TestClient(app)

    first_response = client.post("/api/recommendations/city", json={"citySlug": "kyoto"})
    second_response = client.post("/api/recommendations/city", json={"citySlug": "kyoto"})

    assert first_response.status_code == 200
    assert first_response.json()["status"] in {"generated", "fallback"}
    assert first_response.json()["citySlug"] == "kyoto"
    assert "old-capital" in first_response.json()["groups"][0]["workSlugs"]
    assert second_response.status_code == 200
    assert second_response.json()["status"] == "cached"


def test_city_recommendations_fallback_for_unknown_city() -> None:
    client = TestClient(app)

    response = client.post("/api/recommendations/city", json={"citySlug": "unknown"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "fallback"
    assert payload["groups"] == []
