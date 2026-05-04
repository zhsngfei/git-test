from typing import Any

import httpx

from app.features.collections.repository import SupabaseCollectionsRepository
from app.features.collections.schemas import CollectionCreate


def test_supabase_repository_writes_collection_rows(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    requests: list[dict[str, Any]] = []

    def fake_request(method: str, url: str, **kwargs: Any) -> httpx.Response:
        requests.append({"method": method, "url": url, **kwargs})
        request = httpx.Request(method, url)
        return httpx.Response(
            201,
            request=request,
            json=[
                {
                    "entity_type": "work",
                    "entity_id": "old-capital",
                    "city_slug": "kyoto",
                }
            ],
        )

    monkeypatch.setattr(httpx, "request", fake_request)
    repository = SupabaseCollectionsRepository(
        supabase_url="https://example.supabase.co",
        service_role_key="service-role-key",
    )

    item = repository.add_user_collection(
        "user-id",
        CollectionCreate(entityType="work", entityId="old-capital", citySlug="kyoto"),
    )

    assert item.entityId == "old-capital"
    assert requests[0]["method"] == "POST"
    assert requests[0]["url"] == "https://example.supabase.co/rest/v1/collections"
    assert requests[0]["json"][0] == {
        "user_id": "user-id",
        "entity_type": "work",
        "entity_id": "old-capital",
        "city_slug": "kyoto",
    }
    assert requests[0]["headers"]["Authorization"] == "Bearer service-role-key"


def test_supabase_repository_reads_user_collections(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    def fake_request(method: str, url: str, **kwargs: Any) -> httpx.Response:
        assert method == "GET"
        assert url == "https://example.supabase.co/rest/v1/collections"
        assert kwargs["params"]["user_id"] == "eq.user-id"
        request = httpx.Request(method, url)
        return httpx.Response(
            200,
            request=request,
            json=[
                {
                    "entity_type": "place",
                    "entity_id": "gion",
                    "city_slug": "kyoto",
                }
            ],
        )

    monkeypatch.setattr(httpx, "request", fake_request)
    repository = SupabaseCollectionsRepository(
        supabase_url="https://example.supabase.co",
        service_role_key="service-role-key",
    )

    items = repository.list_user_collections("user-id")

    assert items[0].entityType == "place"
    assert items[0].entityId == "gion"
    assert items[0].citySlug == "kyoto"


def test_supabase_repository_deletes_user_collection(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    requests: list[dict[str, Any]] = []

    def fake_request(method: str, url: str, **kwargs: Any) -> httpx.Response:
        requests.append({"method": method, "url": url, **kwargs})
        return httpx.Response(204, request=httpx.Request(method, url))

    monkeypatch.setattr(httpx, "request", fake_request)
    repository = SupabaseCollectionsRepository(
        supabase_url="https://example.supabase.co",
        service_role_key="service-role-key",
    )

    repository.delete_user_collection("user-id", "work", "old-capital")

    assert requests[0]["method"] == "DELETE"
    assert requests[0]["params"] == {
        "user_id": "eq.user-id",
        "entity_type": "eq.work",
        "entity_id": "eq.old-capital",
    }
