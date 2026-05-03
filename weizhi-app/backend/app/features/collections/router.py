from typing import Annotated

from fastapi import APIRouter, Header, HTTPException, Response, status

from app.features.collections.repository import (
    add_user_collection,
    delete_user_collection,
    list_user_collections,
)
from app.features.collections.schemas import CollectionCreate, CollectionItem, CollectionList, EntityType

router = APIRouter(prefix="/api/collections", tags=["collections"])


@router.get("")
def get_collections(
    user_id: Annotated[str | None, Header(alias="X-Weizhi-User-Id")] = None,
) -> CollectionList:
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    return CollectionList(items=list_user_collections(user_id))


@router.post("", status_code=status.HTTP_201_CREATED)
def create_collection(
    item: CollectionCreate,
    user_id: Annotated[str | None, Header(alias="X-Weizhi-User-Id")] = None,
) -> CollectionItem:
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    return add_user_collection(user_id, item)


@router.delete("/{entity_type}/{entity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_collection(
    entity_type: EntityType,
    entity_id: str,
    user_id: Annotated[str | None, Header(alias="X-Weizhi-User-Id")] = None,
) -> Response:
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")

    delete_user_collection(user_id, entity_type, entity_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
