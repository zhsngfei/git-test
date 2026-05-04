from fastapi.testclient import TestClient
import jwt
from datetime import UTC, datetime, timedelta

from app.core.config import settings
from app.main import app


def make_test_token(user_id: str) -> str:
    return jwt.encode(
        {
            "sub": user_id,
            "aud": "authenticated",
            "iss": f"{settings.supabase_url.rstrip('/')}/auth/v1",
            "role": "authenticated",
            "exp": datetime.now(UTC) + timedelta(minutes=30),
        },
        settings.supabase_jwt_secret,
        algorithm="HS256",
    )


def auth_headers(user_id: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {make_test_token(user_id)}"}


def test_collections_require_bearer_token() -> None:
    client = TestClient(app)

    response = client.get("/api/collections")

    assert response.status_code == 401


def test_collections_reject_legacy_user_header() -> None:
    client = TestClient(app)

    response = client.get(
        "/api/collections",
        headers={"X-Weizhi-User-Id": "legacy-user"},
    )

    assert response.status_code == 401


def test_collections_reject_token_without_expiration() -> None:
    client = TestClient(app)
    token = jwt.encode(
        {
            "sub": "user-no-exp",
            "aud": "authenticated",
            "iss": f"{settings.supabase_url.rstrip('/')}/auth/v1",
            "role": "authenticated",
        },
        settings.supabase_jwt_secret,
        algorithm="HS256",
    )

    response = client.get(
        "/api/collections",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401


def test_collections_reject_token_with_wrong_role() -> None:
    client = TestClient(app)
    token = jwt.encode(
        {
            "sub": "user-wrong-role",
            "aud": "authenticated",
            "iss": f"{settings.supabase_url.rstrip('/')}/auth/v1",
            "role": "anon",
            "exp": datetime.now(UTC) + timedelta(minutes=30),
        },
        settings.supabase_jwt_secret,
        algorithm="HS256",
    )

    response = client.get(
        "/api/collections",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401


def test_user_can_create_and_list_collections() -> None:
    client = TestClient(app)
    headers = auth_headers("user-collections-create")

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
    headers = auth_headers("user-collections-delete")
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
    headers = auth_headers("user-collections-preparation")
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
