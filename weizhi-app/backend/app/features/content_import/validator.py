import csv
from pathlib import Path


REQUIRED_COLUMNS: dict[str, set[str]] = {
    "cities.csv": {"slug", "name_zh", "country_region", "is_supported", "content_depth"},
    "works.csv": {"slug", "title", "work_type", "synopsis", "review_status"},
    "places.csv": {"slug", "city_slug", "name", "intro", "review_status"},
    "work_city_relations.csv": {
        "work_slug",
        "city_slug",
        "relation_summary",
        "recommendation_note",
        "theme_tags",
        "review_status",
    },
    "work_place_relations.csv": {"work_slug", "place_slug", "meaning", "review_status"},
}


def validate_csv_columns(path: Path) -> list[str]:
    required = REQUIRED_COLUMNS[path.name]

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        columns = set(reader.fieldnames or [])

    missing = sorted(required - columns)
    return missing
