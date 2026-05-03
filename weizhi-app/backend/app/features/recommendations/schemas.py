from typing import Literal

from pydantic import BaseModel


ContentTypeFilter = Literal["all", "book", "film"]
RecommendationStatus = Literal["cached", "generated", "fallback"]


class CityRecommendationRequest(BaseModel):
    citySlug: str
    contentType: ContentTypeFilter = "all"


class RecommendationGroup(BaseModel):
    title: str
    workSlugs: list[str]
    placeSlugs: list[str]


class CityRecommendationResponse(BaseModel):
    citySlug: str
    status: RecommendationStatus
    message: str
    groups: list[RecommendationGroup]
