from app.features.cities.repository import get_city_recommendations
from app.features.recommendations.schemas import RecommendationGroup


class MimoAIRecommendationProvider:
    def generate_city_groups(self, city_slug: str, content_type: str) -> list[RecommendationGroup]:
        city_recommendations = get_city_recommendations(city_slug)
        if city_recommendations is None:
            return []

        works = city_recommendations["works"]
        places = city_recommendations["places"]
        if not isinstance(works, list) or not isinstance(places, list):
            return []

        work_slugs = [
            work["slug"]
            for work in works
            if isinstance(work, dict)
            and isinstance(work.get("slug"), str)
            and (content_type == "all" or work.get("contentType") == content_type)
        ]
        place_slugs = [
            place["slug"]
            for place in places
            if isinstance(place, dict) and isinstance(place.get("slug"), str)
        ]

        if not work_slugs and not place_slugs:
            return []

        return [
            RecommendationGroup(
                title="出发前推荐内容",
                workSlugs=work_slugs[:3],
                placeSlugs=place_slugs[:3],
            )
        ]
