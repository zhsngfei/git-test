from app.features.recommendations.provider import MimoAIRecommendationProvider
from app.features.recommendations.schemas import (
    CityRecommendationRequest,
    CityRecommendationResponse,
)

_city_recommendation_cache: dict[str, CityRecommendationResponse] = {}


def get_city_recommendation(
    request: CityRecommendationRequest,
    provider: MimoAIRecommendationProvider | None = None,
) -> CityRecommendationResponse:
    cache_key = f"{request.citySlug}:{request.contentType}"
    cached = _city_recommendation_cache.get(cache_key)
    if cached is not None:
        return cached.model_copy(update={"status": "cached"})

    provider = provider or MimoAIRecommendationProvider()
    groups = provider.generate_city_groups(request.citySlug, request.contentType)
    if not groups:
        return CityRecommendationResponse(
            citySlug=request.citySlug,
            status="fallback",
            message="暂时使用默认推荐，未生成新的推荐分组。",
            groups=[],
        )

    response = CityRecommendationResponse(
        citySlug=request.citySlug,
        status="generated",
        message="已基于已核验内容生成推荐分组。",
        groups=groups,
    )
    _city_recommendation_cache[cache_key] = response
    return response
