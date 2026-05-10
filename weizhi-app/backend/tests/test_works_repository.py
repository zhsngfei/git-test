from app.features.works.repository import SupabaseWorksRepository


class FakeResponse:
    status_code = 200

    def __init__(self, payload: object) -> None:
        self.payload = payload

    def raise_for_status(self) -> None:
        return None

    def json(self) -> object:
        return self.payload


def test_supabase_works_repository_builds_work_detail(monkeypatch) -> None:
    responses = [
        [
            {
                "id": "work-1",
                "slug": "lost-in-translation",
                "title": "迷失东京",
                "original_title": "Lost in Translation",
                "work_type": "film",
                "creator": "Sofia Coppola",
                "year": "2003",
                "synopsis": "在陌生的城市里，寻找连接的可能。",
            }
        ],
        [
            {
                "city_id": "city-1",
                "relation_summary": "东京的酒店、街道与霓虹构成作品的情绪底色。",
                "recommendation_note": "用克制镜头捕捉都市中的疏离与短暂连接。",
            }
        ],
        [
            {
                "id": "city-1",
                "slug": "tokyo",
                "name_zh": "东京",
                "country_region": "日本",
            }
        ],
        [
            {
                "place_id": "place-1",
                "meaning": "新宿帮助用户理解片中陌生城市的明亮、喧嚣与短暂连接。",
            }
        ],
        [
            {
                "id": "place-1",
                "slug": "shinjuku",
                "name": "新宿",
                "intro": "霓虹、人潮和夜间城市经验交汇的地点。",
            }
        ],
    ]
    requests: list[dict[str, object]] = []

    def fake_request(**kwargs):
        requests.append(kwargs)
        return FakeResponse(responses.pop(0))

    monkeypatch.setattr("app.features.works.repository.httpx.request", fake_request)

    repository = SupabaseWorksRepository(
        supabase_url="https://project.supabase.co",
        service_role_key="service-role",
    )

    work_detail = repository.get_work_detail("lost-in-translation")

    assert work_detail == {
        "work": {
            "id": "lost-in-translation",
            "slug": "lost-in-translation",
            "titleZh": "迷失东京",
            "titleOriginal": "Lost in Translation",
            "contentType": "film",
            "creator": "Sofia Coppola",
            "year": "2003",
            "summary": "在陌生的城市里，寻找连接的可能。",
        },
        "city": {
            "slug": "tokyo",
            "nameZh": "东京",
            "countryRegion": "日本",
        },
        "recommendationReason": "用克制镜头捕捉都市中的疏离与短暂连接。",
        "cityConnection": "东京的酒店、街道与霓虹构成作品的情绪底色。",
        "relatedPlaces": [
            {
                "id": "shinjuku",
                "slug": "shinjuku",
                "nameZh": "新宿",
                "summary": "新宿帮助用户理解片中陌生城市的明亮、喧嚣与短暂连接。",
            }
        ],
    }
    assert requests[0]["params"] == {
        "select": "id,slug,title,original_title,work_type,creator,year,synopsis",
        "slug": "eq.lost-in-translation",
        "review_status": "in.(reviewed,published)",
        "limit": "1",
    }
    assert requests[1]["params"] == {
        "select": "city_id,relation_summary,recommendation_note",
        "work_id": "eq.work-1",
        "review_status": "in.(reviewed,published)",
        "order": "id.asc",
        "limit": "1",
    }
    assert requests[3]["params"] == {
        "select": "place_id,meaning",
        "work_id": "eq.work-1",
        "review_status": "in.(reviewed,published)",
        "order": "id.asc",
    }


def test_supabase_works_repository_returns_none_for_unknown_work(monkeypatch) -> None:
    requests: list[dict[str, object]] = []

    def fake_request(**kwargs):
        requests.append(kwargs)
        return FakeResponse([])

    monkeypatch.setattr("app.features.works.repository.httpx.request", fake_request)

    repository = SupabaseWorksRepository(
        supabase_url="https://project.supabase.co",
        service_role_key="service-role",
    )

    assert repository.get_work_detail("unknown") is None
    assert len(requests) == 1
