from pathlib import Path

from app.features.content_import.validator import validate_csv_columns


def test_cities_template_has_required_columns() -> None:
    path = Path("../content/templates/cities.csv").resolve()

    missing = validate_csv_columns(path)

    assert missing == []
