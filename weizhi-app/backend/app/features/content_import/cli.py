import argparse
from pathlib import Path

from app.features.content_import.importer import (
    SupabaseContentImportClient,
    SupabaseContentImporter,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Import reviewed Weizhi content CSV files.")
    parser.add_argument("--directory", required=True, help="Directory containing content CSV files.")
    parser.add_argument("--supabase-url", required=True, help="Supabase project URL.")
    parser.add_argument("--service-role-key", required=True, help="Supabase service role key.")
    args = parser.parse_args(argv)

    client = SupabaseContentImportClient(
        supabase_url=args.supabase_url,
        service_role_key=args.service_role_key,
    )
    importer = SupabaseContentImporter(client=client)
    report = importer.import_directory(Path(args.directory).resolve())

    return 0 if report.is_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
