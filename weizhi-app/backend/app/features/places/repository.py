import httpx

from app.core.config import settings


def get_place_detail(place_slug: str) -> dict[str, object] | None:
    if _should_use_supabase():
        return _supabase_repository().get_place_detail(place_slug)

    place_details: dict[str, dict[str, object]] = {
        "gion": {
            "place": {
                "id": "gion",
                "slug": "gion",
                "nameZh": "祇园",
                "summary": "京都代表性的传统街区之一，与作品中的旧日生活秩序紧密相关。",
            },
            "city": {
                "slug": "kyoto",
                "nameZh": "京都",
                "countryRegion": "日本",
            },
            "meaning": "祇园帮助用户理解《古都》中传统街区、旧日生活秩序和城市记忆之间的关系。",
            "relatedWorks": [
                {
                    "id": "old-capital",
                    "slug": "old-capital",
                    "titleZh": "古都",
                    "contentType": "book",
                    "creator": "川端康成",
                    "summary": "从街巷、季节和传统生活进入京都。",
                }
            ],
        },
        "kamo-river": {
            "place": {
                "id": "kamo-river",
                "slug": "kamo-river",
                "nameZh": "鸭川",
                "summary": "贯穿京都日常生活的河流，也是理解作品中城市关系的地点触点。",
            },
            "city": {
                "slug": "kyoto",
                "nameZh": "京都",
                "countryRegion": "日本",
            },
            "meaning": "鸭川把作品里的城市季节感、散步经验和日常生活连接起来。",
            "relatedWorks": [
                {
                    "id": "old-capital",
                    "slug": "old-capital",
                    "titleZh": "古都",
                    "contentType": "book",
                    "creator": "川端康成",
                    "summary": "从街巷、季节和传统生活进入京都。",
                }
            ],
        },
        "shinjuku": {
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
            "meaning": "新宿帮助用户理解《迷失东京》中陌生城市的明亮、喧嚣与短暂连接。",
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
        },
    }

    return place_details.get(place_slug)


def _should_use_supabase() -> bool:
    return settings.app_env != "local"


def _supabase_repository() -> "SupabasePlacesRepository":
    return SupabasePlacesRepository(
        supabase_url=settings.supabase_url,
        service_role_key=settings.supabase_service_role_key,
    )


class SupabasePlacesRepository:
    def __init__(self, supabase_url: str, service_role_key: str) -> None:
        self.base_url = f"{supabase_url.rstrip('/')}/rest/v1"
        self.headers = {
            "apikey": service_role_key,
            "Authorization": f"Bearer {service_role_key}",
            "Content-Type": "application/json",
        }

    def get_place_detail(self, place_slug: str) -> dict[str, object] | None:
        place_rows = self._request(
            "GET",
            "/places",
            params={
                "select": "id,slug,city_id,name,intro",
                "slug": f"eq.{place_slug}",
                "review_status": "in.(reviewed,published)",
                "limit": "1",
            },
        )
        if not place_rows:
            return None

        place = place_rows[0]
        city_rows = self._request(
            "GET",
            "/cities",
            params={
                "select": "id,slug,name_zh,country_region",
                "id": f"eq.{place['city_id']}",
                "is_supported": "eq.true",
                "limit": "1",
            },
        )
        if not city_rows:
            return None

        relation_rows = self._request(
            "GET",
            "/work_place_relations",
            params={
                "select": "work_id,meaning",
                "place_id": f"eq.{place['id']}",
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

        city = city_rows[0]
        return {
            "place": {
                "id": place["slug"],
                "slug": place["slug"],
                "nameZh": place["name"],
                "summary": place["intro"],
            },
            "city": {
                "slug": city["slug"],
                "nameZh": city["name_zh"],
                "countryRegion": city["country_region"],
            },
            "meaning": _place_meaning(place, relation_rows),
            "relatedWorks": [_map_related_work(row) for row in work_rows],
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


def _place_meaning(place: dict[str, object], relation_rows: list[dict[str, object]]) -> object:
    if relation_rows:
        return relation_rows[0]["meaning"]

    return place["intro"]


def _map_related_work(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row["slug"],
        "slug": row["slug"],
        "titleZh": row["title"],
        "contentType": row["work_type"],
        "creator": row.get("creator") or "",
        "summary": row["synopsis"],
    }
