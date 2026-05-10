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
    assert report.files[0].issues == []


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


def test_validate_import_directory_reports_invalid_values_and_references() -> None:
    directory = Path("tests/fixtures/content_import/invalid_values").resolve()

    report = validate_import_directory(directory)

    assert report.is_ready is False
    assert report.total_files == 5
    assert report.total_rows == 6
    issues = {
        file.name: file.issues
        for file in report.files
    }
    assert issues["cities.csv"] == [
        "row 3: slug 'kyoto' is duplicated",
        "row 3: content_depth must be one of core, expansion, unsupported",
        "row 3: is_supported must be one of true or false",
    ]
    assert issues["works.csv"] == [
        "row 2: title is required",
        "row 2: work_type must be one of book, film, series",
        "row 2: review_status must be one of draft, published, reviewed",
    ]
    assert issues["places.csv"] == [
        "row 2: city_slug references missing city 'missing-city'",
        "row 2: review_status must be one of draft, published, reviewed",
    ]
    assert issues["work_city_relations.csv"] == [
        "row 2: work_slug references missing work 'missing-work'",
        "row 2: city_slug references missing city 'missing-city'",
    ]
    assert issues["work_place_relations.csv"] == [
        "row 2: work_slug references missing work 'missing-work'",
        "row 2: place_slug references missing place 'missing-place'",
    ]
