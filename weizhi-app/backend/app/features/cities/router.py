from fastapi import APIRouter

from app.features.cities.repository import list_supported_cities

router = APIRouter(prefix="/api/cities", tags=["cities"])


@router.get("")
def get_supported_cities() -> list[dict[str, str | bool]]:
    return list_supported_cities()
