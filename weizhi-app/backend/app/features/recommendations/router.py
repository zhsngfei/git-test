from fastapi import APIRouter

from app.features.recommendations.schemas import CityRecommendationRequest, CityRecommendationResponse
from app.features.recommendations.service import get_city_recommendation

router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])


@router.post("/city")
def recommend_city(request: CityRecommendationRequest) -> CityRecommendationResponse:
    return get_city_recommendation(request)
