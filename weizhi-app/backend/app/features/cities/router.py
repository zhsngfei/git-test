from fastapi import APIRouter, HTTPException

from app.features.cities.repository import get_city_recommendations, list_supported_cities

router = APIRouter(prefix="/api/cities", tags=["cities"])


@router.get("")
def get_supported_cities() -> list[dict[str, str | bool]]:
    return list_supported_cities()


@router.get("/{city_slug}/recommendations")
def get_recommendations(city_slug: str) -> dict[str, object]:
    recommendations = get_city_recommendations(city_slug)
    if recommendations is None:
        raise HTTPException(status_code=404, detail="City recommendations not found")

    return recommendations
