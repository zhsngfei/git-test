from fastapi import APIRouter, HTTPException

from app.features.works.repository import get_work_detail

router = APIRouter(prefix="/api/works", tags=["works"])


@router.get("/{work_slug}")
def get_work(work_slug: str) -> dict[str, object]:
    work = get_work_detail(work_slug)
    if work is None:
        raise HTTPException(status_code=404, detail="Work not found")

    return work
