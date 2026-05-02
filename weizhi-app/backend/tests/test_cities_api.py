from fastapi.testclient import TestClient

from app.main import app


def test_list_supported_cities_returns_seed_shape() -> None:
    client = TestClient(app)
    response = client.get("/api/cities")

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert payload[0]["slug"] == "kyoto"
    assert payload[0]["nameZh"] == "京都"
