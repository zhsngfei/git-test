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

ALLOWED_VALUES: dict[str, dict[str, set[str]]] = {
    "cities.csv": {
        "content_depth": {"core", "expansion", "unsupported"},
        "is_supported": {"true", "false"},
    },
    "works.csv": {
        "work_type": {"book", "film", "series"},
        "review_status": {"draft", "reviewed", "published"},
    },
    "places.csv": {
        "review_status": {"draft", "reviewed", "published"},
    },
    "work_city_relations.csv": {
        "review_status": {"draft", "reviewed", "published"},
    },
    "work_place_relations.csv": {
        "review_status": {"draft", "reviewed", "published"},
    },
}

SLUG_COLUMNS: dict[str, str] = {
    "cities.csv": "slug",
    "works.csv": "slug",
    "places.csv": "slug",
}


@dataclass(frozen=True)
class CsvValidationResult:
    name: str
    row_count: int
    missing_columns: list[str]
    issues: list[str]

    @property
    def is_ready(self) -> bool:
        return not self.missing_columns and not self.issues


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
    rows_by_file = {
        file_name: _read_csv_rows(directory / file_name)
        for file_name in REQUIRED_COLUMNS
        if (directory / file_name).exists()
    }
    slug_sets = _collect_slug_sets(rows_by_file)
    results = []
    for file_name in REQUIRED_COLUMNS:
        path = directory / file_name
        if path.exists():
            results.append(
                validate_csv_file(
                    path,
                    rows=rows_by_file[file_name],
                    slug_sets=slug_sets,
                )
            )

    return ImportValidationReport(files=results)


def validate_csv_file(
    path: Path,
    *,
    rows: list[dict[str, str]] | None = None,
    slug_sets: dict[str, set[str]] | None = None,
) -> CsvValidationResult:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        columns = set(reader.fieldnames or [])
        csv_rows = rows if rows is not None else list(reader)

    missing = sorted(REQUIRED_COLUMNS[path.name] - columns)
    issues = [] if missing else _validate_rows(path.name, csv_rows, slug_sets or {})
    return CsvValidationResult(
        name=path.name,
        row_count=len(csv_rows),
        missing_columns=missing,
        issues=issues,
    )


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def _collect_slug_sets(rows_by_file: dict[str, list[dict[str, str]]]) -> dict[str, set[str]]:
    return {
        file_name: {
            row[column].strip()
            for row in rows
            if row.get(column, "").strip()
        }
        for file_name, column in SLUG_COLUMNS.items()
        if (rows := rows_by_file.get(file_name))
    }


def _validate_rows(
    file_name: str,
    rows: list[dict[str, str]],
    slug_sets: dict[str, set[str]],
) -> list[str]:
    issues: list[str] = []
    issues.extend(_required_value_issues(file_name, rows))
    issues.extend(_duplicate_slug_issues(file_name, rows))
    issues.extend(_reference_issues(file_name, rows, slug_sets))
    issues.extend(_allowed_value_issues(file_name, rows))
    return issues


def _required_value_issues(file_name: str, rows: list[dict[str, str]]) -> list[str]:
    issues: list[str] = []
    for index, row in enumerate(rows, start=2):
        for column in sorted(REQUIRED_COLUMNS[file_name]):
            if not row.get(column, "").strip():
                issues.append(f"row {index}: {column} is required")

    return issues


def _allowed_value_issues(file_name: str, rows: list[dict[str, str]]) -> list[str]:
    issues: list[str] = []
    for index, row in enumerate(rows, start=2):
        for column, allowed_values in ALLOWED_VALUES.get(file_name, {}).items():
            value = row.get(column, "").strip()
            if value and value not in allowed_values:
                allowed = (
                    "true or false"
                    if allowed_values == {"true", "false"}
                    else ", ".join(sorted(allowed_values))
                )
                issues.append(f"row {index}: {column} must be one of {allowed}")

    return issues


def _duplicate_slug_issues(file_name: str, rows: list[dict[str, str]]) -> list[str]:
    slug_column = SLUG_COLUMNS.get(file_name)
    if slug_column is None:
        return []

    seen: set[str] = set()
    issues: list[str] = []
    for index, row in enumerate(rows, start=2):
        slug = row.get(slug_column, "").strip()
        if not slug:
            continue
        if slug in seen:
            issues.append(f"row {index}: slug '{slug}' is duplicated")
        seen.add(slug)

    return issues


def _reference_issues(
    file_name: str,
    rows: list[dict[str, str]],
    slug_sets: dict[str, set[str]],
) -> list[str]:
    if file_name == "places.csv":
        return _missing_reference_issues(rows, "city_slug", "city", slug_sets.get("cities.csv", set()))
    if file_name == "work_city_relations.csv":
        return (
            _missing_reference_issues(rows, "work_slug", "work", slug_sets.get("works.csv", set()))
            + _missing_reference_issues(rows, "city_slug", "city", slug_sets.get("cities.csv", set()))
        )
    if file_name == "work_place_relations.csv":
        return (
            _missing_reference_issues(rows, "work_slug", "work", slug_sets.get("works.csv", set()))
            + _missing_reference_issues(rows, "place_slug", "place", slug_sets.get("places.csv", set()))
        )

    return []


def _missing_reference_issues(
    rows: list[dict[str, str]],
    column: str,
    label: str,
    known_slugs: set[str],
) -> list[str]:
    issues: list[str] = []
    for index, row in enumerate(rows, start=2):
        slug = row.get(column, "").strip()
        if slug and slug not in known_slugs:
            issues.append(f"row {index}: {column} references missing {label} '{slug}'")

    return issues
