from app.features.places.repository import SupabasePlacesRepository


class FakeResponse:
    status_code = 200

    def __init__(self, payload: object) -> None:
        self.payload = payload

    def raise_for_status(self) -> None:
        return None

    def json(self) -> object:
        return self.payload


def test_supabase_places_repository_builds_place_detail(monkeypatch) -> None:
    responses = [
        [
            {
                "id": "place-1",
                "slug": "shinjuku",
                "city_id": "city-1",
                "name": "新宿",
                "intro": "霓虹、人潮和夜间城市经验交汇的地点。",
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
                "work_id": "work-1",
                "meaning": "新宿帮助用户理解片中陌生城市的明亮、喧嚣与短暂连接。",
            }
        ],
        [
            {
                "id": "work-1",
                "slug": "lost-in-translation",
                "title": "迷失东京",
                "work_type": "film",
                "creator": "Sofia Coppola",
                "synopsis": "在陌生的城市里，寻找连接的可能。",
            }
        ],
    ]
    requests: list[dict[str, object]] = []

    def fake_request(**kwargs):
        requests.append(kwargs)
        return FakeResponse(responses.pop(0))

    monkeypatch.setattr("app.features.places.repository.httpx.request", fake_request)

    repository = SupabasePlacesRepository(
        supabase_url="https://project.supabase.co",
        service_role_key="service-role",
    )

    place_detail = repository.get_place_detail("shinjuku")

    assert place_detail == {
        "place": {
            "id": "shinjuku",
            "slug": "shinjuku",
            "nameZh": "新宿",
            "summary": "霓虹、人潮和夜间城市经验交汇的地点。",
        },
        "city": {
            "slug": "tokyo",
            "nameZh": "东京",
            "countryRegion": "日本",
        },
        "meaning": "新宿帮助用户理解片中陌生城市的明亮、喧嚣与短暂连接。",
        "relatedWorks": [
            {
                "id": "lost-in-translation",
                "slug": "lost-in-translation",
                "titleZh": "迷失东京",
                "contentType": "film",
                "creator": "Sofia Coppola",
                "summary": "在陌生的城市里，寻找连接的可能。",
            }
        ],
    }
    assert requests[0]["params"] == {
        "select": "id,slug,city_id,name,intro",
        "slug": "eq.shinjuku",
        "review_status": "in.(reviewed,published)",
        "limit": "1",
    }
    assert requests[1]["params"] == {
        "select": "id,slug,name_zh,country_region",
        "id": "eq.city-1",
        "is_supported": "eq.true",
        "limit": "1",
    }
    assert requests[2]["params"] == {
        "select": "work_id,meaning",
        "place_id": "eq.place-1",
        "review_status": "in.(reviewed,published)",
        "order": "id.asc",
    }


def test_supabase_places_repository_returns_none_for_unknown_place(monkeypatch) -> None:
    requests: list[dict[str, object]] = []

    def fake_request(**kwargs):
        requests.append(kwargs)
        return FakeResponse([])

    monkeypatch.setattr("app.features.places.repository.httpx.request", fake_request)

    repository = SupabasePlacesRepository(
        supabase_url="https://project.supabase.co",
        service_role_key="service-role",
    )

    assert repository.get_place_detail("unknown") is None
    assert len(requests) == 1
