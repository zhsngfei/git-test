import httpx

from app.core.config import settings


def list_supported_cities() -> list[dict[str, str | bool]]:
    if _should_use_supabase():
        return _supabase_repository().list_supported_cities()

    return [
        {
            "slug": "kyoto",
            "nameZh": "京都",
            "countryRegion": "日本",
            "isSupported": True,
            "contentDepth": "core",
            "toneSummary": "从作品、街区和地点关系开始认识这座城市",
        },
        {
            "slug": "tokyo",
            "nameZh": "东京",
            "countryRegion": "日本",
            "isSupported": True,
            "contentDepth": "core",
            "toneSummary": "孤独、夜晚、现代都市与日常缝隙",
        },
    ]


def get_city_recommendations(city_slug: str) -> dict[str, object] | None:
    if _should_use_supabase():
        return _supabase_repository().get_city_recommendations(city_slug)

    recommendations: dict[str, dict[str, object]] = {
        "kyoto": {
            "city": {
                "slug": "kyoto",
                "nameZh": "京都",
                "countryRegion": "日本",
                "intro": "从作品、街区和地点关系开始认识这座城市。",
            },
            "contentTypes": [
                {"value": "all", "label": "全部"},
                {"value": "book", "label": "书籍"},
                {"value": "film", "label": "电影"},
            ],
            "featuredWork": {
                "id": "old-capital",
                "slug": "old-capital",
                "titleZh": "古都",
                "contentType": "book",
                "creator": "川端康成",
                "summary": "从季节、街巷和传统生活里，看见京都更缓慢的一面。",
                "placeCount": 2,
            },
            "works": [
                {
                    "id": "old-capital",
                    "slug": "old-capital",
                    "titleZh": "古都",
                    "contentType": "book",
                    "creator": "川端康成",
                    "summary": "一部通过京都街巷和传统生活气息进入城市记忆的小说。",
                    "placeCount": 2,
                },
                {
                    "id": "like-father-like-son",
                    "slug": "like-father-like-son",
                    "titleZh": "如父如子",
                    "contentType": "film",
                    "creator": "是枝裕和",
                    "summary": "从家庭关系进入城市日常。",
                    "placeCount": 1,
                },
            ],
            "places": [
                {
                    "id": "gion",
                    "slug": "gion",
                    "nameZh": "祇园",
                    "summary": "理解传统街区和旧日生活秩序的入口。",
                    "relatedWorkCount": 1,
                },
                {
                    "id": "kamo-river",
                    "slug": "kamo-river",
                    "nameZh": "鸭川",
                    "summary": "连接京都日常和作品中的城市经验。",
                    "relatedWorkCount": 1,
                },
            ],
        },
        "tokyo": {
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
                "placeCount": 2,
            },
            "works": [
                {
                    "id": "lost-in-translation",
                    "slug": "lost-in-translation",
                    "titleZh": "迷失东京",
                    "contentType": "film",
                    "creator": "Sofia Coppola",
                    "summary": "在陌生的城市里，寻找连接的可能。",
                    "placeCount": 2,
                },
                {
                    "id": "norwegian-wood",
                    "slug": "norwegian-wood",
                    "titleZh": "挪威的森林",
                    "contentType": "book",
                    "creator": "村上春树",
                    "summary": "从记忆、青春和城市日常进入东京。",
                    "placeCount": 1,
                },
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
        },
    }

    return recommendations.get(city_slug)


def _should_use_supabase() -> bool:
    return settings.app_env != "local"


def _supabase_repository() -> "SupabaseCitiesRepository":
    return SupabaseCitiesRepository(
        supabase_url=settings.supabase_url,
        service_role_key=settings.supabase_service_role_key,
    )


class SupabaseCitiesRepository:
    def __init__(self, supabase_url: str, service_role_key: str) -> None:
        self.base_url = f"{supabase_url.rstrip('/')}/rest/v1"
        self.headers = {
            "apikey": service_role_key,
            "Authorization": f"Bearer {service_role_key}",
            "Content-Type": "application/json",
        }

    def list_supported_cities(self) -> list[dict[str, str | bool]]:
        rows = self._request(
            "GET",
            "/cities",
            params={
                "select": "slug,name_zh,country_region,is_supported,content_depth,tone_summary",
                "is_supported": "eq.true",
                "order": "slug.asc",
            },
        )
        return [
            {
                "slug": row["slug"],
                "nameZh": row["name_zh"],
                "countryRegion": row["country_region"],
                "isSupported": row["is_supported"],
                "contentDepth": row["content_depth"],
                "toneSummary": row.get("tone_summary") or "",
            }
            for row in rows
        ]

    def get_city_recommendations(self, city_slug: str) -> dict[str, object] | None:
        city_rows = self._request(
            "GET",
            "/cities",
            params={
                "select": "id,slug,name_zh,country_region,tone_summary",
                "slug": f"eq.{city_slug}",
                "is_supported": "eq.true",
                "limit": "1",
            },
        )
        if not city_rows:
            return None

        city = city_rows[0]
        city_id = city["id"]
        relation_rows = self._request(
            "GET",
            "/work_city_relations",
            params={
                "select": "work_id,recommendation_note",
                "city_id": f"eq.{city_id}",
                "review_status": "in.(reviewed,published)",
                "order": "id.asc",
            },
        )
        work_ids = [row["work_id"] for row in relation_rows]
        if work_ids:
            work_rows = self._request(
                "GET",
                "/works",
                params={
                    "select": "id,slug,title,work_type,creator,synopsis",
                    "id": f"in.({_comma_join(work_ids)})",
                    "review_status": "in.(reviewed,published)",
                },
            )
        else:
            work_rows = []
        place_rows = self._request(
            "GET",
            "/places",
            params={
                "select": "id,slug,name,intro",
                "city_id": f"eq.{city_id}",
                "review_status": "in.(reviewed,published)",
                "order": "name.asc",
            },
        )
        if work_ids:
            relation_place_rows = self._request(
                "GET",
                "/work_place_relations",
                params={
                    "select": "work_id,place_id",
                    "work_id": f"in.({_comma_join(work_ids)})",
                    "review_status": "in.(reviewed,published)",
                },
            )
        else:
            relation_place_rows = []

        notes_by_work_id = {
            relation["work_id"]: relation["recommendation_note"] for relation in relation_rows
        }
        place_count_by_work_id: dict[str, int] = {}
        related_count_by_place_id: dict[str, int] = {}
        for relation in relation_place_rows:
            place_count_by_work_id[relation["work_id"]] = (
                place_count_by_work_id.get(relation["work_id"], 0) + 1
            )
            related_count_by_place_id[relation["place_id"]] = (
                related_count_by_place_id.get(relation["place_id"], 0) + 1
            )

        works = [
            _map_work_for_city_page(
                row,
                notes_by_work_id.get(row["id"]) or row["synopsis"],
                place_count_by_work_id.get(row["id"], 0),
            )
            for row in work_rows
        ]
        places = [
            {
                "id": row["slug"],
                "slug": row["slug"],
                "nameZh": row["name"],
                "summary": row["intro"],
                "relatedWorkCount": related_count_by_place_id.get(row["id"], 0),
            }
            for row in place_rows
        ]

        return {
            "city": {
                "slug": city["slug"],
                "nameZh": city["name_zh"],
                "countryRegion": city["country_region"],
                "intro": city.get("tone_summary") or "",
            },
            "contentTypes": [
                {"value": "all", "label": "全部"},
                {"value": "book", "label": "书籍"},
                {"value": "film", "label": "电影"},
            ],
            "featuredWork": works[0] if works else None,
            "works": works,
            "places": places,
        }

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, str] | None = None,
    ) -> object:
        response = httpx.request(
            method=method,
            url=f"{self.base_url}{path}",
            headers=self.headers,
            params=params,
            timeout=10.0,
        )
        response.raise_for_status()
        return response.json()


def _comma_join(values: list[str]) -> str:
    return ",".join(values)


def _map_work_for_city_page(
    row: dict[str, object],
    summary: str,
    place_count: int,
) -> dict[str, object]:
    return {
        "id": row["slug"],
        "slug": row["slug"],
        "titleZh": row["title"],
        "contentType": row["work_type"],
        "creator": row.get("creator") or "",
        "summary": summary,
        "placeCount": place_count,
    }
