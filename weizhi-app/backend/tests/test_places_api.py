from fastapi.testclient import TestClient

from app.main import app


def test_get_place_detail_returns_city_meaning_and_related_works() -> None:
    client = TestClient(app)
    response = client.get("/api/places/gion")

    assert response.status_code == 200
    payload = response.json()
    assert payload["place"]["slug"] == "gion"
    assert payload["place"]["nameZh"] == "祇园"
    assert payload["city"]["slug"] == "kyoto"
    assert payload["meaning"]
    assert payload["relatedWorks"][0]["slug"] == "old-capital"


def test_get_place_detail_returns_404_for_unknown_place() -> None:
    client = TestClient(app)
    response = client.get("/api/places/unknown")

    assert response.status_code == 404
