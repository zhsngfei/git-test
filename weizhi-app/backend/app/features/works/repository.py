import httpx

from app.core.config import settings


def get_work_detail(work_slug: str) -> dict[str, object] | None:
    if _should_use_supabase():
        return _supabase_repository().get_work_detail(work_slug)

    work_details: dict[str, dict[str, object]] = {
        "old-capital": {
            "work": {
                "id": "old-capital",
                "slug": "old-capital",
                "titleZh": "古都",
                "titleOriginal": "古都",
                "contentType": "book",
                "creator": "川端康成",
                "year": "1962",
                "summary": "一部通过京都街巷、季节和传统生活气息进入城市记忆的小说。",
            },
            "city": {
                "slug": "kyoto",
                "nameZh": "京都",
                "countryRegion": "日本",
            },
            "recommendationReason": "它不急着解释京都，而是让用户先习惯这座城市的留白、秩序和季节感。",
            "cityConnection": "作品中的京都不是背景板，而是人物生活方式、家族记忆和城市秩序的一部分。",
            "relatedPlaces": [
                {
                    "id": "gion",
                    "slug": "gion",
                    "nameZh": "祇园",
                    "summary": "理解传统街区和旧日生活秩序的入口。",
                },
                {
                    "id": "kamo-river",
                    "slug": "kamo-river",
                    "nameZh": "鸭川",
                    "summary": "连接京都日常和作品中的城市经验。",
                },
            ],
        },
        "lost-in-translation": {
            "work": {
                "id": "lost-in-translation",
                "slug": "lost-in-translation",
                "titleZh": "迷失东京",
                "titleOriginal": "Lost in Translation",
                "contentType": "film",
                "creator": "Sofia Coppola",
                "year": "2003",
                "summary": "一部以东京酒店、街道和夜晚经验为主要城市线索的电影。",
            },
            "city": {
                "slug": "tokyo",
                "nameZh": "东京",
                "countryRegion": "日本",
            },
            "recommendationReason": "它用克制的镜头语言捕捉都市中的异乡感、疏离与短暂连接。",
            "cityConnection": "片中的酒店、酒吧、街道与霓虹构成了东京的夜间层次。",
            "relatedPlaces": [
                {
                    "id": "shinjuku",
                    "slug": "shinjuku",
                    "nameZh": "新宿",
                    "summary": "霓虹、人潮和夜间城市经验交汇的地点。",
                }
            ],
        },
    }

    return work_details.get(work_slug)


def _should_use_supabase() -> bool:
    return settings.app_env != "local"


def _supabase_repository() -> "SupabaseWorksRepository":
    return SupabaseWorksRepository(
        supabase_url=settings.supabase_url,
        service_role_key=settings.supabase_service_role_key,
    )


class SupabaseWorksRepository:
    def __init__(self, supabase_url: str, service_role_key: str) -> None:
        self.base_url = f"{supabase_url.rstrip('/')}/rest/v1"
        self.headers = {
            "apikey": service_role_key,
            "Authorization": f"Bearer {service_role_key}",
            "Content-Type": "application/json",
        }

    def get_work_detail(self, work_slug: str) -> dict[str, object] | None:
        work_rows = self._request(
            "GET",
            "/works",
            params={
                "select": "id,slug,title,original_title,work_type,creator,year,synopsis",
                "slug": f"eq.{work_slug}",
                "review_status": "in.(reviewed,published)",
                "limit": "1",
            },
        )
        if not work_rows:
            return None

        work = work_rows[0]
        relation_rows = self._request(
            "GET",
            "/work_city_relations",
            params={
                "select": "city_id,relation_summary,recommendation_note",
                "work_id": f"eq.{work['id']}",
                "review_status": "in.(reviewed,published)",
                "order": "id.asc",
                "limit": "1",
            },
        )
        if not relation_rows:
            return None

        city_relation = relation_rows[0]
        city_rows = self._request(
            "GET",
            "/cities",
            params={
                "select": "id,slug,name_zh,country_region",
                "id": f"eq.{city_relation['city_id']}",
                "is_supported": "eq.true",
                "limit": "1",
            },
        )
        if not city_rows:
            return None

        place_relation_rows = self._request(
            "GET",
            "/work_place_relations",
            params={
                "select": "place_id,meaning",
                "work_id": f"eq.{work['id']}",
                "review_status": "in.(reviewed,published)",
                "order": "id.asc",
            },
        )
        place_ids = [row["place_id"] for row in place_relation_rows]
        if place_ids:
            place_rows = self._request(
                "GET",
                "/places",
                params={
                    "select": "id,slug,name,intro",
                    "id": f"in.({_comma_join(place_ids)})",
                    "review_status": "in.(reviewed,published)",
                },
            )
        else:
            place_rows = []

        city = city_rows[0]
        meaning_by_place_id = {
            relation["place_id"]: relation["meaning"] for relation in place_relation_rows
        }
        return {
            "work": _map_work_detail(work),
            "city": {
                "slug": city["slug"],
                "nameZh": city["name_zh"],
                "countryRegion": city["country_region"],
            },
            "recommendationReason": city_relation["recommendation_note"],
            "cityConnection": city_relation["relation_summary"],
            "relatedPlaces": [
                {
                    "id": row["slug"],
                    "slug": row["slug"],
                    "nameZh": row["name"],
                    "summary": meaning_by_place_id.get(row["id"]) or row["intro"],
                }
                for row in place_rows
            ],
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


def _map_work_detail(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row["slug"],
        "slug": row["slug"],
        "titleZh": row["title"],
        "titleOriginal": row.get("original_title") or "",
        "contentType": row["work_type"],
        "creator": row.get("creator") or "",
        "year": row.get("year") or "",
        "summary": row["synopsis"],
    }
