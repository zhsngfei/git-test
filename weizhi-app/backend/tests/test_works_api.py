from fastapi.testclient import TestClient

from app.main import app


def test_get_work_detail_returns_city_and_related_places() -> None:
    client = TestClient(app)
    response = client.get("/api/works/old-capital")

    assert response.status_code == 200
    payload = response.json()
    assert payload["work"]["slug"] == "old-capital"
    assert payload["work"]["titleZh"] == "古都"
    assert payload["work"]["contentType"] == "book"
    assert payload["city"]["slug"] == "kyoto"
    assert payload["recommendationReason"]
    assert payload["cityConnection"]
    assert payload["relatedPlaces"][0]["slug"] == "gion"


def test_get_work_detail_returns_404_for_unknown_work() -> None:
    client = TestClient(app)
    response = client.get("/api/works/unknown")

    assert response.status_code == 404
