from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from app.features.auth.dependencies import AuthenticatedUser, get_current_user
from app.features.collections.repository import (
    add_user_collection,
    build_preparation_book,
    delete_user_collection,
    list_user_collections,
)
from app.features.collections.schemas import (
    CollectionCreate,
    CollectionItem,
    CollectionList,
    EntityType,
    PreparationBook,
)

router = APIRouter(prefix="/api/collections", tags=["collections"])


@router.get("")
def get_collections(
    user: Annotated[AuthenticatedUser, Depends(get_current_user)],
) -> CollectionList:
    return CollectionList(items=list_user_collections(user.user_id))


@router.get("/preparation")
def get_preparation_book(
    user: Annotated[AuthenticatedUser, Depends(get_current_user)],
) -> PreparationBook:
    return build_preparation_book(user.user_id)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_collection(
    item: CollectionCreate,
    user: Annotated[AuthenticatedUser, Depends(get_current_user)],
) -> CollectionItem:
    return add_user_collection(user.user_id, item)


@router.delete("/{entity_type}/{entity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_collection(
    entity_type: EntityType,
    entity_id: str,
    user: Annotated[AuthenticatedUser, Depends(get_current_user)],
) -> Response:
    delete_user_collection(user.user_id, entity_type, entity_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
