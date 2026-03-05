import argparse
from pathlib import Path
import pandas as pd


def generate_report(csv_path: str, output_path: str) -> None:
    df = pd.read_csv(csv_path)

    if "amount" not in df.columns:
        raise ValueError("CSV must contain an 'amount' column.")

    total = df["amount"].sum()
    count = len(df)

    lines = []
    lines.append("# Daily Report")
    lines.append("")
    lines.append(f"- Rows: **{count}**")
    lines.append(f"- Total amount: **{total}**")

    if "product" in df.columns:
        top = df.groupby("product")["amount"].sum().sort_values(ascending=False).head(1)
        if not top.empty:
            lines.append(f"- Top product: **{top.index[0]}** (**{float(top.iloc[0])}**)")

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ Report written to {output_path}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Generate a simple markdown report from a CSV.")
    ap.add_argument("--csv", required=True)
    ap.add_argument("--output", default="output/report.md")
    args = ap.parse_args()

    generate_report(args.csv, args.output)