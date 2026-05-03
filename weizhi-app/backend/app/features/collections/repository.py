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
    return _collections_by_user.get(user_id, [])


def add_user_collection(user_id: str, item: CollectionCreate) -> CollectionItem:
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
