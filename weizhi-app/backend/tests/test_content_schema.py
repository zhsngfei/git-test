import pytest
from pydantic import ValidationError

from app.schemas.content import CityRecord, ContentDepth, ReviewStatus, WorkRecord, WorkType


def test_city_record_accepts_supported_core_city() -> None:
    city = CityRecord(
        slug="kyoto",
        name_zh="京都",
        country_region="日本",
        is_supported=True,
        content_depth=ContentDepth.core,
    )

    assert city.slug == "kyoto"


def test_work_record_requires_synopsis() -> None:
    with pytest.raises(ValidationError):
        WorkRecord(
            slug="empty",
            title="空作品",
            work_type=WorkType.book,
            synopsis="",
            review_status=ReviewStatus.reviewed,
        )
