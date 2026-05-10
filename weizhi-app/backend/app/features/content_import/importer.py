import csv
from pathlib import Path
from typing import Protocol

import httpx

from app.features.content_import.validator import ImportValidationReport, validate_import_directory


class ContentImportClient(Protocol):
    def upsert(self, table: str, rows: list[dict[str, object]]) -> list[dict[str, object]]:
        pass


class SupabaseContentImportClient:
    def __init__(self, supabase_url: str, service_role_key: str) -> None:
        self.base_url = f"{supabase_url.rstrip('/')}/rest/v1"
        self.headers = {
            "apikey": service_role_key,
            "Authorization": f"Bearer {service_role_key}",
            "Content-Type": "application/json",
        }

    def upsert(self, table: str, rows: list[dict[str, object]]) -> list[dict[str, object]]:
        if not rows:
            return []

        response = httpx.request(
            method="POST",
            url=f"{self.base_url}/{table}",
            headers={
                **self.headers,
                "Prefer": "resolution=merge-duplicates,return=representation",
            },
            params={"on_conflict": _on_conflict_for_table(table)},
            json=rows,
            timeout=10.0,
        )
        response.raise_for_status()
        return response.json()


class SupabaseContentImporter:
    def __init__(self, client: ContentImportClient) -> None:
        self.client = client

    def import_directory(self, directory: Path) -> ImportValidationReport:
        report = validate_import_directory(directory)
        if not report.is_ready:
            return report

        cities = _read_rows(directory / "cities.csv")
        works = _read_rows(directory / "works.csv")
        places = _read_rows(directory / "places.csv")
        work_city_relations = _read_rows(directory / "work_city_relations.csv")
        work_place_relations = _read_rows(directory / "work_place_relations.csv")

        city_ids = self._upsert_with_slug_index("cities", [_map_city(row) for row in cities])
        work_ids = self._upsert_with_slug_index("works", [_map_work(row) for row in works])
        place_ids = self._upsert_with_slug_index(
            "places",
            [_map_place(row, city_ids) for row in places],
        )
        self.client.upsert(
            "work_city_relations",
            [_map_work_city_relation(row, city_ids, work_ids) for row in work_city_relations],
        )
        self.client.upsert(
            "work_place_relations",
            [_map_work_place_relation(row, place_ids, work_ids) for row in work_place_relations],
        )
        return report

    def _upsert_with_slug_index(
        self,
        table: str,
        rows: list[dict[str, object]],
    ) -> dict[str, str]:
        response_rows = self.client.upsert(table, rows)
        return {
            str(row["slug"]): str(row["id"])
            for row in response_rows
            if row.get("slug") and row.get("id")
        }


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def _map_city(row: dict[str, str]) -> dict[str, object]:
    return {
        "slug": _value(row, "slug"),
        "name_zh": _value(row, "name_zh"),
        "name_en": _optional_value(row, "name_en"),
        "country_region": _value(row, "country_region"),
        "is_supported": _boolean_value(row, "is_supported"),
        "content_depth": _value(row, "content_depth"),
        "tone_summary": _optional_value(row, "tone_summary"),
        "hero_image_url": _optional_value(row, "hero_image_url"),
    }


def _map_work(row: dict[str, str]) -> dict[str, object]:
    return {
        "slug": _value(row, "slug"),
        "title": _value(row, "title"),
        "original_title": _optional_value(row, "original_title"),
        "work_type": _value(row, "work_type"),
        "creator": _optional_value(row, "creator"),
        "year": _optional_value(row, "year"),
        "synopsis": _value(row, "synopsis"),
        "cover_image_url": _optional_value(row, "cover_image_url"),
        "review_status": _value(row, "review_status"),
    }


def _map_place(row: dict[str, str], city_ids: dict[str, str]) -> dict[str, object]:
    return {
        "slug": _value(row, "slug"),
        "city_id": city_ids[_value(row, "city_slug")],
        "name": _value(row, "name"),
        "intro": _value(row, "intro"),
        "image_url": _optional_value(row, "image_url"),
        "address": _optional_value(row, "address"),
        "latitude": _optional_value(row, "latitude"),
        "longitude": _optional_value(row, "longitude"),
        "map_query": _optional_value(row, "map_query"),
        "review_status": _value(row, "review_status"),
    }


def _map_work_city_relation(
    row: dict[str, str],
    city_ids: dict[str, str],
    work_ids: dict[str, str],
) -> dict[str, object]:
    return {
        "work_id": work_ids[_value(row, "work_slug")],
        "city_id": city_ids[_value(row, "city_slug")],
        "relation_summary": _value(row, "relation_summary"),
        "recommendation_note": _value(row, "recommendation_note"),
        "source_url": _optional_value(row, "source_url"),
        "source_note": _optional_value(row, "source_note"),
        "review_status": _value(row, "review_status"),
    }


def _map_work_place_relation(
    row: dict[str, str],
    place_ids: dict[str, str],
    work_ids: dict[str, str],
) -> dict[str, object]:
    return {
        "work_id": work_ids[_value(row, "work_slug")],
        "place_id": place_ids[_value(row, "place_slug")],
        "meaning": _value(row, "meaning"),
        "source_url": _optional_value(row, "source_url"),
        "source_note": _optional_value(row, "source_note"),
        "review_status": _value(row, "review_status"),
    }


def _value(row: dict[str, str], key: str) -> str:
    return row[key].strip()


def _optional_value(row: dict[str, str], key: str) -> str | None:
    value = row.get(key, "").strip()
    return value or None


def _boolean_value(row: dict[str, str], key: str) -> bool:
    return _value(row, key).lower() == "true"


def _on_conflict_for_table(table: str) -> str:
    if table in {"cities", "works", "places"}:
        return "slug"
    if table == "work_city_relations":
        return "work_id,city_id"
    if table == "work_place_relations":
        return "work_id,place_id"

    raise ValueError(f"Unsupported import table: {table}")
