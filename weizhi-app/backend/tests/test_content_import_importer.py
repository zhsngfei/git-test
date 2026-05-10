from pathlib import Path

from app.features.content_import.importer import SupabaseContentImporter


class FakeSupabaseContentClient:
    def __init__(self) -> None:
        self.calls: list[tuple[str, list[dict[str, object]]]] = []
        self.ids_by_table_and_slug = {
            "cities": {
                "kyoto": "city-kyoto",
                "tokyo": "city-tokyo",
            },
            "works": {
                "old-capital": "work-old-capital",
                "lost-in-translation": "work-lost-in-translation",
            },
            "places": {
                "gion": "place-gion",
                "kamo-river": "place-kamo-river",
            },
        }

    def upsert(self, table: str, rows: list[dict[str, object]]) -> list[dict[str, object]]:
        self.calls.append((table, rows))
        return [
            {
                "id": self.ids_by_table_and_slug.get(table, {}).get(str(row["slug"]), f"{table}-{index}"),
                "slug": row["slug"],
            }
            for index, row in enumerate(rows)
            if "slug" in row
        ]


def test_importer_upserts_content_in_dependency_order() -> None:
    client = FakeSupabaseContentClient()
    importer = SupabaseContentImporter(client=client)

    result = importer.import_directory(Path("../content/templates").resolve())

    assert result.is_ready is True
    assert result.total_rows == 10
    assert [table for table, _rows in client.calls] == [
        "cities",
        "works",
        "places",
        "work_city_relations",
        "work_place_relations",
    ]
    assert client.calls[0][1][0] == {
        "slug": "kyoto",
        "name_zh": "京都",
        "name_en": "Kyoto",
        "country_region": "日本",
        "is_supported": True,
        "content_depth": "core",
        "tone_summary": "从作品、街区和地点关系开始认识这座城市",
        "hero_image_url": None,
    }
    assert client.calls[2][1][0]["city_id"] == "city-kyoto"
    assert client.calls[3][1][0]["work_id"] == "work-old-capital"
    assert client.calls[3][1][0]["city_id"] == "city-kyoto"
    assert client.calls[4][1][0]["work_id"] == "work-old-capital"
    assert client.calls[4][1][0]["place_id"] == "place-gion"


def test_importer_refuses_to_upsert_invalid_directory() -> None:
    client = FakeSupabaseContentClient()
    importer = SupabaseContentImporter(client=client)

    result = importer.import_directory(Path("tests/fixtures/content_import/invalid_values").resolve())

    assert result.is_ready is False
    assert result.total_rows == 6
    assert client.calls == []
