from pathlib import Path

from app.features.content_import import cli


class FakeReport:
    is_ready = True
    total_files = 5
    total_rows = 10


class FakeImporter:
    def __init__(self, client: object) -> None:
        self.client = client

    def import_directory(self, directory: Path) -> FakeReport:
        cli_calls.append(("import_directory", directory))
        return FakeReport()


class FakeClient:
    def __init__(self, supabase_url: str, service_role_key: str) -> None:
        cli_calls.append(("client", supabase_url, service_role_key))


cli_calls: list[tuple[object, ...]] = []


def test_cli_runs_content_import_with_configured_client(monkeypatch) -> None:
    cli_calls.clear()
    monkeypatch.setattr(cli, "SupabaseContentImportClient", FakeClient)
    monkeypatch.setattr(cli, "SupabaseContentImporter", FakeImporter)

    exit_code = cli.main(
        [
            "--directory",
            "../content/templates",
            "--supabase-url",
            "https://project.supabase.co",
            "--service-role-key",
            "service-role",
        ]
    )

    assert exit_code == 0
    assert cli_calls == [
        ("client", "https://project.supabase.co", "service-role"),
        ("import_directory", Path("../content/templates").resolve()),
    ]
