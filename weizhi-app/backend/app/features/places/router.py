from fastapi import APIRouter, HTTPException

from app.features.places.repository import get_place_detail

router = APIRouter(prefix="/api/places", tags=["places"])


@router.get("/{place_slug}")
def get_place(place_slug: str) -> dict[str, object]:
    place = get_place_detail(place_slug)
    if place is None:
        raise HTTPException(status_code=404, detail="Place not found")

    return place
