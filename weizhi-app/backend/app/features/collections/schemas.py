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


class PreparationCity(BaseModel):
    slug: str
    nameZh: str
    countryRegion: str | None = None


class PreparationWork(BaseModel):
    id: str
    slug: str
    titleZh: str
    contentType: Literal["book", "film", "series"]
    summary: str | None = None


class PreparationPlace(BaseModel):
    id: str
    slug: str
    nameZh: str
    summary: str | None = None


class PreparationCityGroup(BaseModel):
    city: PreparationCity
    works: list[PreparationWork]
    places: list[PreparationPlace]


class PreparationBook(BaseModel):
    cities: list[PreparationCityGroup]
