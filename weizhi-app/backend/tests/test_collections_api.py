from fastapi.testclient import TestClient

from app.main import app


def test_collections_require_user_header() -> None:
    client = TestClient(app)

    response = client.get("/api/collections")

    assert response.status_code == 401


def test_user_can_create_and_list_collections() -> None:
    client = TestClient(app)
    headers = {"X-Weizhi-User-Id": "user-collections-create"}

    create_response = client.post(
        "/api/collections",
        headers=headers,
        json={"entityType": "work", "entityId": "old-capital", "citySlug": "kyoto"},
    )
    list_response = client.get("/api/collections", headers=headers)

    assert create_response.status_code == 201
    assert create_response.json()["entityId"] == "old-capital"
    assert list_response.status_code == 200
    assert list_response.json()["items"][0]["entityType"] == "work"


def test_user_can_delete_collection_item() -> None:
    client = TestClient(app)
    headers = {"X-Weizhi-User-Id": "user-collections-delete"}
    client.post(
        "/api/collections",
        headers=headers,
        json={"entityType": "place", "entityId": "gion", "citySlug": "kyoto"},
    )

    delete_response = client.delete("/api/collections/place/gion", headers=headers)
    list_response = client.get("/api/collections", headers=headers)

    assert delete_response.status_code == 204
    assert list_response.json()["items"] == []


def test_user_can_view_preparation_book_grouped_by_city() -> None:
    client = TestClient(app)
    headers = {"X-Weizhi-User-Id": "user-collections-preparation"}
    client.post(
        "/api/collections",
        headers=headers,
        json={"entityType": "work", "entityId": "old-capital", "citySlug": "kyoto"},
    )
    client.post(
        "/api/collections",
        headers=headers,
        json={"entityType": "place", "entityId": "gion", "citySlug": "kyoto"},
    )

    response = client.get("/api/collections/preparation", headers=headers)

    assert response.status_code == 200
    payload = response.json()
    assert payload["cities"][0]["city"]["slug"] == "kyoto"
    assert payload["cities"][0]["works"][0]["slug"] == "old-capital"
    assert payload["cities"][0]["places"][0]["slug"] == "gion"
