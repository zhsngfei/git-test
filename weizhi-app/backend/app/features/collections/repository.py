from app.features.collections.schemas import CollectionCreate, CollectionItem, EntityType

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
