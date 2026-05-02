from enum import StrEnum

from pydantic import BaseModel, Field


class WorkType(StrEnum):
    book = "book"
    film = "film"
    series = "series"


class ReviewStatus(StrEnum):
    draft = "draft"
    reviewed = "reviewed"
    published = "published"


class ContentDepth(StrEnum):
    core = "core"
    expansion = "expansion"
    unsupported = "unsupported"


class CityRecord(BaseModel):
    slug: str
    name_zh: str
    name_en: str | None = None
    country_region: str
    is_supported: bool
    content_depth: ContentDepth
    tone_summary: str | None = None
    hero_image_url: str | None = None


class WorkRecord(BaseModel):
    slug: str
    title: str
    original_title: str | None = None
    work_type: WorkType
    creator: str | None = None
    year: str | None = None
    synopsis: str = Field(min_length=1)
    cover_image_url: str | None = None
    review_status: ReviewStatus


class PlaceRecord(BaseModel):
    slug: str
    city_slug: str
    name: str
    intro: str = Field(min_length=1)
    image_url: str | None = None
    address: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    map_query: str | None = None
    review_status: ReviewStatus
