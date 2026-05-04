import httpx

from app.core.config import settings
from app.features.collections.schemas import (
    CollectionCreate,
    CollectionItem,
    EntityType,
    PreparationBook,
    PreparationCity,
    PreparationCityGroup,
    PreparationPlace,
    PreparationWork,
)

_collections_by_user: dict[str, list[CollectionItem]] = {}


def list_user_collections(user_id: str) -> list[CollectionItem]:
    if _should_use_supabase():
        return _supabase_repository().list_user_collections(user_id)

    return _collections_by_user.get(user_id, [])


def add_user_collection(user_id: str, item: CollectionCreate) -> CollectionItem:
    if _should_use_supabase():
        return _supabase_repository().add_user_collection(user_id, item)

    collection_item = CollectionItem(
        entityType=item.entityType,
        entityId=item.entityId,
        citySlug=item.citySlug,
    )
    user_items = _collections_by_user.setdefault(user_id, [])

    existing_index = next(
        (
            index
            for index, existing in enumerate(user_items)
            if existing.entityType == collection_item.entityType
            and existing.entityId == collection_item.entityId
        ),
        None,
    )
    if existing_index is not None:
        user_items[existing_index] = collection_item
        return collection_item

    user_items.append(collection_item)
    return collection_item


def delete_user_collection(user_id: str, entity_type: EntityType, entity_id: str) -> None:
    if _should_use_supabase():
        _supabase_repository().delete_user_collection(user_id, entity_type, entity_id)
        return

    user_items = _collections_by_user.get(user_id, [])
    _collections_by_user[user_id] = [
        item
        for item in user_items
        if not (item.entityType == entity_type and item.entityId == entity_id)
    ]


def build_preparation_book(user_id: str) -> PreparationBook:
    groups_by_city: dict[str, PreparationCityGroup] = {}
    for item in list_user_collections(user_id):
        group = groups_by_city.setdefault(
            item.citySlug,
            PreparationCityGroup(
                city=_city_for_slug(item.citySlug),
                works=[],
                places=[],
            ),
        )
        if item.entityType == "work":
            group.works.append(_work_for_id(item.entityId))
        else:
            group.places.append(_place_for_id(item.entityId))

    return PreparationBook(cities=list(groups_by_city.values()))


def _city_for_slug(city_slug: str) -> PreparationCity:
    cities = {
        "kyoto": PreparationCity(slug="kyoto", nameZh="京都", countryRegion="日本"),
        "tokyo": PreparationCity(slug="tokyo", nameZh="东京", countryRegion="日本"),
    }
    return cities.get(city_slug, PreparationCity(slug=city_slug, nameZh=city_slug))


def _work_for_id(entity_id: str) -> PreparationWork:
    works = {
        "old-capital": PreparationWork(
            id="old-capital",
            slug="old-capital",
            titleZh="古都",
            contentType="book",
            summary="从街巷、季节和传统生活进入京都。",
        ),
        "lost-in-translation": PreparationWork(
            id="lost-in-translation",
            slug="lost-in-translation",
            titleZh="迷失东京",
            contentType="film",
            summary="在陌生的城市里，寻找连接的可能。",
        ),
    }
    return works.get(
        entity_id,
        PreparationWork(id=entity_id, slug=entity_id, titleZh=entity_id, contentType="book"),
    )


def _place_for_id(entity_id: str) -> PreparationPlace:
    places = {
        "gion": PreparationPlace(
            id="gion",
            slug="gion",
            nameZh="祇园",
            summary="理解传统街区和旧日生活秩序的入口。",
        ),
        "kamo-river": PreparationPlace(
            id="kamo-river",
            slug="kamo-river",
            nameZh="鸭川",
            summary="连接京都日常和作品中的城市经验。",
        ),
        "shinjuku": PreparationPlace(
            id="shinjuku",
            slug="shinjuku",
            nameZh="新宿",
            summary="霓虹、人潮和夜间城市经验交汇的地点。",
        ),
    }
    return places.get(
        entity_id,
        PreparationPlace(id=entity_id, slug=entity_id, nameZh=entity_id),
    )


def _should_use_supabase() -> bool:
    return settings.app_env != "local"


def _supabase_repository() -> "SupabaseCollectionsRepository":
    return SupabaseCollectionsRepository(
        supabase_url=settings.supabase_url,
        service_role_key=settings.supabase_service_role_key,
    )


class SupabaseCollectionsRepository:
    def __init__(self, supabase_url: str, service_role_key: str) -> None:
        self.base_url = f"{supabase_url.rstrip('/')}/rest/v1"
        self.headers = {
            "apikey": service_role_key,
            "Authorization": f"Bearer {service_role_key}",
            "Content-Type": "application/json",
        }

    def list_user_collections(self, user_id: str) -> list[CollectionItem]:
        rows = self._request(
            "GET",
            "/collections",
            params={
                "select": "entity_type,entity_id,city_slug",
                "user_id": f"eq.{user_id}",
                "order": "created_at.asc",
            },
        )
        return [
            CollectionItem(
                entityType=row["entity_type"],
                entityId=row["entity_id"],
                citySlug=row["city_slug"],
            )
            for row in rows
        ]

    def add_user_collection(self, user_id: str, item: CollectionCreate) -> CollectionItem:
        rows = self._request(
            "POST",
            "/collections",
            params={"on_conflict": "user_id,entity_type,entity_id"},
            json=[
                {
                    "user_id": user_id,
                    "entity_type": item.entityType,
                    "entity_id": item.entityId,
                    "city_slug": item.citySlug,
                }
            ],
            extra_headers={"Prefer": "resolution=merge-duplicates,return=representation"},
        )
        row = rows[0]
        return CollectionItem(
            entityType=row["entity_type"],
            entityId=row["entity_id"],
            citySlug=row["city_slug"],
        )

    def delete_user_collection(self, user_id: str, entity_type: EntityType, entity_id: str) -> None:
        self._request(
            "DELETE",
            "/collections",
            params={
                "user_id": f"eq.{user_id}",
                "entity_type": f"eq.{entity_type}",
                "entity_id": f"eq.{entity_id}",
            },
        )

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, str] | None = None,
        json: object | None = None,
        extra_headers: dict[str, str] | None = None,
    ) -> object:
        response = httpx.request(
            method,
            f"{self.base_url}{path}",
            headers={**self.headers, **(extra_headers or {})},
            params=params,
            json=json,
            timeout=10.0,
        )
        response.raise_for_status()
        if response.status_code == 204:
            return []

        return response.json()
