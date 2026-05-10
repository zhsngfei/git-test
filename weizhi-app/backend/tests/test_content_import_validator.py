from pathlib import Path

from app.features.content_import.validator import validate_csv_columns, validate_import_directory


def test_cities_template_has_required_columns() -> None:
    path = Path("../content/templates/cities.csv").resolve()

    missing = validate_csv_columns(path)

    assert missing == []


def test_validate_import_directory_reports_ready_templates() -> None:
    directory = Path("../content/templates").resolve()

    report = validate_import_directory(directory)

    assert report.is_ready is True
    assert report.total_files == 5
    assert report.total_rows == 10
    assert [file.name for file in report.files] == [
        "cities.csv",
        "works.csv",
        "places.csv",
        "work_city_relations.csv",
        "work_place_relations.csv",
    ]
    assert report.files[0].row_count == 2
    assert report.files[0].missing_columns == []


def test_validate_import_directory_reports_missing_columns() -> None:
    directory = Path("tests/fixtures/content_import/incomplete").resolve()

    report = validate_import_directory(directory)

    assert report.is_ready is False
    assert report.total_files == 1
    assert report.total_rows == 1
    assert report.files[0].name == "cities.csv"
    assert report.files[0].missing_columns == [
        "content_depth",
        "country_region",
        "is_supported",
    ]
