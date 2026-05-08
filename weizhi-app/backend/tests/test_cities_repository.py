from app.features.cities.repository import SupabaseCitiesRepository


class FakeResponse:
    status_code = 200

    def __init__(self, payload: object) -> None:
        self.payload = payload

    def raise_for_status(self) -> None:
        return None

    def json(self) -> object:
        return self.payload


def test_supabase_cities_repository_lists_supported_cities(monkeypatch) -> None:
    requests: list[dict[str, object]] = []

    def fake_request(**kwargs):
        requests.append(kwargs)
        return FakeResponse(
            [
                {
                    "slug": "tokyo",
                    "name_zh": "东京",
                    "country_region": "日本",
                    "is_supported": True,
                    "content_depth": "core",
                    "tone_summary": "现代都市、日常生活与作品中的地点线索。",
                }
            ]
        )

    monkeypatch.setattr("app.features.cities.repository.httpx.request", fake_request)

    repository = SupabaseCitiesRepository(
        supabase_url="https://project.supabase.co",
        service_role_key="service-role",
    )

    cities = repository.list_supported_cities()

    assert cities == [
        {
            "slug": "tokyo",
            "nameZh": "东京",
            "countryRegion": "日本",
            "isSupported": True,
            "contentDepth": "core",
            "toneSummary": "现代都市、日常生活与作品中的地点线索。",
        }
    ]
    assert requests == [
        {
            "method": "GET",
            "url": "https://project.supabase.co/rest/v1/cities",
            "headers": {
                "apikey": "service-role",
                "Authorization": "Bearer service-role",
                "Content-Type": "application/json",
            },
            "params": {
                "select": "slug,name_zh,country_region,is_supported,content_depth,tone_summary",
                "is_supported": "eq.true",
                "order": "slug.asc",
            },
            "timeout": 10.0,
        }
    ]


def test_supabase_cities_repository_builds_city_recommendations(monkeypatch) -> None:
    responses = [
        [
            {
                "id": "city-1",
                "slug": "tokyo",
                "name_zh": "东京",
                "country_region": "日本",
                "tone_summary": "现代都市、日常生活与作品中的地点线索。",
            }
        ],
        [
            {
                "work_id": "work-1",
                "recommendation_note": "在陌生的城市里，寻找连接的可能。",
            },
            {
                "work_id": "work-draft",
                "recommendation_note": "草稿内容不应该出现在推荐页。",
            },
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
        [
            {
                "id": "place-1",
                "slug": "shinjuku",
                "name": "新宿",
                "intro": "霓虹、人潮和夜间城市经验交汇的地点。",
            }
        ],
        [
            {
                "work_id": "work-1",
                "place_id": "place-1",
            }
        ],
    ]
    requests: list[dict[str, object]] = []

    def fake_request(**kwargs):
        requests.append(kwargs)
        return FakeResponse(responses.pop(0))

    monkeypatch.setattr("app.features.cities.repository.httpx.request", fake_request)

    repository = SupabaseCitiesRepository(
        supabase_url="https://project.supabase.co",
        service_role_key="service-role",
    )

    recommendations = repository.get_city_recommendations("tokyo")

    assert recommendations == {
        "city": {
            "slug": "tokyo",
            "nameZh": "东京",
            "countryRegion": "日本",
            "intro": "现代都市、日常生活与作品中的地点线索。",
        },
        "contentTypes": [
            {"value": "all", "label": "全部"},
            {"value": "book", "label": "书籍"},
            {"value": "film", "label": "电影"},
        ],
        "featuredWork": {
            "id": "lost-in-translation",
            "slug": "lost-in-translation",
            "titleZh": "迷失东京",
            "contentType": "film",
            "creator": "Sofia Coppola",
            "summary": "在陌生的城市里，寻找连接的可能。",
            "placeCount": 1,
        },
        "works": [
            {
                "id": "lost-in-translation",
                "slug": "lost-in-translation",
                "titleZh": "迷失东京",
                "contentType": "film",
                "creator": "Sofia Coppola",
                "summary": "在陌生的城市里，寻找连接的可能。",
                "placeCount": 1,
            }
        ],
        "places": [
            {
                "id": "shinjuku",
                "slug": "shinjuku",
                "nameZh": "新宿",
                "summary": "霓虹、人潮和夜间城市经验交汇的地点。",
                "relatedWorkCount": 1,
            }
        ],
    }
    assert requests[0]["params"] == {
        "select": "id,slug,name_zh,country_region,tone_summary",
        "slug": "eq.tokyo",
        "is_supported": "eq.true",
        "limit": "1",
    }
    assert requests[1]["params"] == {
        "select": "work_id,recommendation_note",
        "city_id": "eq.city-1",
        "review_status": "in.(reviewed,published)",
        "order": "id.asc",
    }
    assert requests[2]["params"] == {
        "select": "id,slug,title,work_type,creator,synopsis",
        "id": "in.(work-1,work-draft)",
        "review_status": "in.(reviewed,published)",
    }


def test_supabase_cities_repository_returns_none_for_unknown_city(monkeypatch) -> None:
    requests: list[dict[str, object]] = []

    def fake_request(**kwargs):
        requests.append(kwargs)
        return FakeResponse([])

    monkeypatch.setattr("app.features.cities.repository.httpx.request", fake_request)

    repository = SupabaseCitiesRepository(
        supabase_url="https://project.supabase.co",
        service_role_key="service-role",
    )

    assert repository.get_city_recommendations("unknown") is None
    assert len(requests) == 1


def test_supabase_cities_repository_handles_city_without_work_relations(monkeypatch) -> None:
    responses = [
        [
            {
                "id": "city-empty",
                "slug": "nara",
                "name_zh": "奈良",
                "country_region": "日本",
                "tone_summary": "从古寺和街巷进入城市。",
            }
        ],
        [],
        [],
    ]
    requests: list[dict[str, object]] = []

    def fake_request(**kwargs):
        requests.append(kwargs)
        return FakeResponse(responses.pop(0))

    monkeypatch.setattr("app.features.cities.repository.httpx.request", fake_request)

    repository = SupabaseCitiesRepository(
        supabase_url="https://project.supabase.co",
        service_role_key="service-role",
    )

    recommendations = repository.get_city_recommendations("nara")

    assert recommendations == {
        "city": {
            "slug": "nara",
            "nameZh": "奈良",
            "countryRegion": "日本",
            "intro": "从古寺和街巷进入城市。",
        },
        "contentTypes": [
            {"value": "all", "label": "全部"},
            {"value": "book", "label": "书籍"},
            {"value": "film", "label": "电影"},
        ],
        "featuredWork": None,
        "works": [],
        "places": [],
    }
    assert len(requests) == 3
    assert requests[2]["url"] == "https://project.supabase.co/rest/v1/places"
