import csv
from dataclasses import dataclass
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
        "review_status",
    },
    "work_place_relations.csv": {"work_slug", "place_slug", "meaning", "review_status"},
}


@dataclass(frozen=True)
class CsvValidationResult:
    name: str
    row_count: int
    missing_columns: list[str]

    @property
    def is_ready(self) -> bool:
        return not self.missing_columns


@dataclass(frozen=True)
class ImportValidationReport:
    files: list[CsvValidationResult]

    @property
    def total_files(self) -> int:
        return len(self.files)

    @property
    def total_rows(self) -> int:
        return sum(file.row_count for file in self.files)

    @property
    def is_ready(self) -> bool:
        return all(file.is_ready for file in self.files)


def validate_csv_columns(path: Path) -> list[str]:
    required = REQUIRED_COLUMNS[path.name]

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        columns = set(reader.fieldnames or [])

    missing = sorted(required - columns)
    return missing


def validate_import_directory(directory: Path) -> ImportValidationReport:
    results = [
        validate_csv_file(directory / file_name)
        for file_name in REQUIRED_COLUMNS
        if (directory / file_name).exists()
    ]
    return ImportValidationReport(files=results)


def validate_csv_file(path: Path) -> CsvValidationResult:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        columns = set(reader.fieldnames or [])
        row_count = sum(1 for _ in reader)

    missing = sorted(REQUIRED_COLUMNS[path.name] - columns)
    return CsvValidationResult(
        name=path.name,
        row_count=row_count,
        missing_columns=missing,
    )
