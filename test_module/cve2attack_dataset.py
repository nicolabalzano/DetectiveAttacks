import argparse
import csv
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATASET_DIR = REPO_ROOT / "CVE2ATT-CK"
DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parent / "results"


def _read_csv(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _load_split(dataset_dir, split, use_extended_train=False):
    if split == "train" and use_extended_train:
        x_path = dataset_dir / "final_extended_X_train.csv"
        y_path = dataset_dir / "final_extended_y_train.csv"
    else:
        x_path = dataset_dir / f"X_{split}.csv"
        y_path = dataset_dir / f"y_{split}.csv"

    x_rows = _read_csv(x_path)
    y_rows = _read_csv(y_path)
    if len(x_rows) != len(y_rows):
        raise ValueError(f"{x_path.name} and {y_path.name} have different row counts")

    rows = []
    for index, (x_row, y_row) in enumerate(zip(x_rows, y_rows)):
        gold_categories = [
            category
            for category, value in y_row.items()
            if str(value).strip() not in ("", "0", "0.0", "False", "false")
        ]
        rows.append(
            {
                "cve_id": x_row["Name"].strip().replace("_", "-"),
                "description": x_row["Text"].strip(),
                "gold_categories": gold_categories,
                "split": split,
                "source_row": index,
            }
        )
    return rows


def load_cve2attack(dataset_dir=DEFAULT_DATASET_DIR, use_extended_train=False):
    dataset_dir = Path(dataset_dir)
    return merge_duplicate_cves(load_cve2attack_raw(dataset_dir, use_extended_train=use_extended_train))


def load_cve2attack_raw(dataset_dir=DEFAULT_DATASET_DIR, use_extended_train=False):
    dataset_dir = Path(dataset_dir)
    rows = []
    rows.extend(_load_split(dataset_dir, "train", use_extended_train=use_extended_train))
    rows.extend(_load_split(dataset_dir, "test", use_extended_train=False))
    return rows


def merge_duplicate_cves(rows):
    merged = {}
    order = []
    for row in rows:
        cve_id = row["cve_id"]
        if cve_id not in merged:
            merged[cve_id] = {
                "cve_id": cve_id,
                "description": row["description"],
                "gold_categories": [],
                "splits": [],
                "source_rows": [],
            }
            order.append(cve_id)

        target = merged[cve_id]
        for category in row["gold_categories"]:
            if category not in target["gold_categories"]:
                target["gold_categories"].append(category)
        if row["split"] not in target["splits"]:
            target["splits"].append(row["split"])
        target["source_rows"].append({"split": row["split"], "row": row["source_row"]})

        if len(row["description"]) > len(target["description"]):
            target["description"] = row["description"]

    return [merged[cve_id] for cve_id in order]


def write_jsonl(rows, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_csv(rows, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["cve_id", "splits", "gold_categories", "description", "source_rows"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "cve_id": row["cve_id"],
                    "splits": "; ".join(row["splits"]),
                    "gold_categories": "; ".join(row["gold_categories"]),
                    "description": row["description"],
                    "source_rows": json.dumps(row["source_rows"], ensure_ascii=False),
                }
            )


def write_duplicates_report(raw_rows, path):
    by_cve = {}
    for row in raw_rows:
        by_cve.setdefault(row["cve_id"], []).append(row)

    duplicates = {cve_id: rows for cve_id, rows in by_cve.items() if len(rows) > 1}
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["cve_id", "occurrences", "splits", "gold_categories_by_occurrence", "merged_gold_categories"],
        )
        writer.writeheader()
        for cve_id, rows in sorted(duplicates.items()):
            merged_categories = []
            for row in rows:
                for category in row["gold_categories"]:
                    if category not in merged_categories:
                        merged_categories.append(category)
            writer.writerow(
                {
                    "cve_id": cve_id,
                    "occurrences": len(rows),
                    "splits": "; ".join(row["split"] for row in rows),
                    "gold_categories_by_occurrence": " | ".join(
                        "; ".join(row["gold_categories"]) for row in rows
                    ),
                    "merged_gold_categories": "; ".join(merged_categories),
                }
            )


def main():
    parser = argparse.ArgumentParser(
        description="Unifica train e test di CVE2ATT&CK senza convertire le categorie gold in ID ATT&CK."
    )
    parser.add_argument("--dataset-dir", type=Path, default=DEFAULT_DATASET_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument(
        "--use-extended-train",
        action="store_true",
        help="Usa final_extended_X/y_train.csv invece dello split train originale.",
    )
    args = parser.parse_args()

    raw_rows = load_cve2attack_raw(args.dataset_dir, use_extended_train=args.use_extended_train)
    rows = merge_duplicate_cves(raw_rows)
    jsonl_path = args.output_dir / "cve2attack_unified.jsonl"
    csv_path = args.output_dir / "cve2attack_unified.csv"
    duplicates_path = args.output_dir / "cve2attack_duplicates.csv"
    write_jsonl(rows, jsonl_path)
    write_csv(rows, csv_path)
    write_duplicates_report(raw_rows, duplicates_path)
    print(f"Raw rows: {len(raw_rows)}")
    print(f"Unified CVEs: {len(rows)}")
    print(f"JSONL: {jsonl_path}")
    print(f"CSV: {csv_path}")
    print(f"Duplicates: {duplicates_path}")


if __name__ == "__main__":
    main()
