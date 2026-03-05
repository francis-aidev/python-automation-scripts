import argparse
from pathlib import Path
import pandas as pd


def merge_csvs(folder: str, output: str) -> None:
    p = Path(folder)
    csvs = sorted(p.glob("*.csv"))
    if not csvs:
        raise ValueError(f"No CSV files found in {folder}")

    frames = []
    for f in csvs:
        df = pd.read_csv(f)
        df["__source_file"] = f.name
        frames.append(df)

    merged = pd.concat(frames, ignore_index=True)
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(output, index=False)
    print(f"✅ Merged {len(csvs)} files into {output} ({len(merged)} rows)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Merge CSV files in a folder into one CSV.")
    ap.add_argument("--folder", required=True)
    ap.add_argument("--output", default="output/merged.csv")
    args = ap.parse_args()

    merge_csvs(args.folder, args.output)