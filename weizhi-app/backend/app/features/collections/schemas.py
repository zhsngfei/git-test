from typing import Literal

from pydantic import BaseModel


EntityType = Literal["work", "place"]


class CollectionCreate(BaseModel):
    entityType: EntityType
    entityId: str
    citySlug: str


class CollectionItem(BaseModel):
    entityType: EntityType
    entityId: str
    citySlug: str


class CollectionList(BaseModel):
    items: list[CollectionItem]
