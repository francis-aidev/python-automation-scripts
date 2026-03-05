import argparse
from pathlib import Path


def rename_files(folder: str, prefix: str, start: int, dry_run: bool) -> None:
    p = Path(folder)
    if not p.exists() or not p.is_dir():
        raise ValueError(f"Folder not found: {folder}")

    files = sorted([f for f in p.iterdir() if f.is_file()])
    if not files:
        print("No files found.")
        return

    counter = start
    for f in files:
        new_name = f"{prefix}{counter}{f.suffix}"
        target = f.with_name(new_name)

        if dry_run:
            print(f"DRY RUN: {f.name} -> {target.name}")
        else:
            f.rename(target)
            print(f"Renamed: {f.name} -> {target.name}")

        counter += 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Bulk rename files in a folder.")
    ap.add_argument("--folder", required=True)
    ap.add_argument("--prefix", required=True, help="Example: photo_")
    ap.add_argument("--start", type=int, default=1)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    rename_files(args.folder, args.prefix, args.start, args.dry_run)