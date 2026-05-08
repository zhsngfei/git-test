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


def test_local_dev_auth_token_can_access_collections_without_supabase_keys() -> None:
    client = TestClient(app)

    auth_response = client.post(
        "/api/dev/auth/session",
        json={"email": "reader@example.com"},
    )

    assert auth_response.status_code == 201
    auth_payload = auth_response.json()
    assert auth_payload["user"]["email"] == "reader@example.com"
    assert auth_payload["user"]["id"]
    assert "replace-with-service-role-key" not in auth_response.text
    assert "replace-with-supabase-jwt-secret" not in auth_response.text

    headers = {"Authorization": f"Bearer {auth_payload['accessToken']}"}
    create_response = client.post(
        "/api/collections",
        headers=headers,
        json={"entityType": "place", "entityId": "shinjuku", "citySlug": "tokyo"},
    )
    list_response = client.get("/api/collections", headers=headers)

    assert create_response.status_code == 201
    assert list_response.status_code == 200
    assert list_response.json()["items"][0]["entityId"] == "shinjuku"


def test_local_dev_auth_rejects_empty_email() -> None:
    client = TestClient(app)

    response = client.post("/api/dev/auth/session", json={"email": ""})

    assert response.status_code == 422


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
