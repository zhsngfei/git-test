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


def test_get_city_recommendations_returns_content_groups() -> None:
    client = TestClient(app)
    response = client.get("/api/cities/kyoto/recommendations")

    assert response.status_code == 200
    payload = response.json()
    assert payload["city"]["slug"] == "kyoto"
    assert payload["contentTypes"] == [
        {"value": "all", "label": "全部"},
        {"value": "book", "label": "书籍"},
        {"value": "film", "label": "电影"},
    ]
    assert payload["featuredWork"]["titleZh"] == "古都"
    assert payload["works"][0]["contentType"] == "book"
    assert payload["places"][0]["nameZh"] == "祇园"


def test_get_city_recommendations_returns_404_for_unknown_city() -> None:
    client = TestClient(app)
    response = client.get("/api/cities/unknown/recommendations")

    assert response.status_code == 404
