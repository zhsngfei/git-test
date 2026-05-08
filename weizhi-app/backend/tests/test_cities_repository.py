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
