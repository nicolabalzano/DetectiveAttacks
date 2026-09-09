import argparse
import csv
import json
from pathlib import Path
from statistics import mean, median


TEST_MODULE_DIR = Path(__file__).resolve().parent
DEFAULT_PREDICTIONS = (
    TEST_MODULE_DIR
    / "results"
    / "nim_100_full"
    / "predictions_mistralai_mistral_large_3_675b_instruct_2512.jsonl"
)


def safe_div(numerator, denominator):
    return numerator / denominator if denominator else 0.0


def f1_score(precision, recall):
    return safe_div(2 * precision * recall, precision + recall)


def read_jsonl(path):
    with Path(path).open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def category_matches_for_patterns(patterns, gold_categories, limit=None):
    gold = set(gold_categories)
    matched = set()
    selected = patterns if limit is None else patterns[:limit]
    for pattern in selected:
        names = [pattern.get("name", "")]
        if pattern.get("parent_name"):
            names.append(pattern["parent_name"])
        for name in names:
            if name in gold:
                matched.add(name)
    return matched


def row_counts(row):
    comparison = row.get("category_comparison") or {}
    matched = set(comparison.get("matched_gold_categories_by_name", []))
    false_negatives = set(comparison.get("unmatched_gold_categories", []))
    false_positive_ids = set(comparison.get("predicted_ids_not_matching_gold_category_names", []))
    return {
        "tp": len(matched),
        "fp": len(false_positive_ids),
        "fn": len(false_negatives),
        "matched": sorted(matched),
        "false_negatives": sorted(false_negatives),
        "false_positive_ids": sorted(false_positive_ids),
        "exact_match": not false_negatives and not false_positive_ids,
    }


def aggregate(rows):
    tp = fp = fn = 0
    exact = 0
    any_hit = 0
    per_precision = []
    per_recall = []
    per_f1 = []
    topk_micro_hits = {1: 0, 3: 0, 5: 0}
    topk_macro = {1: [], 3: [], 5: []}
    total_gold = 0

    for row in rows:
        counts = row_counts(row)
        tp += counts["tp"]
        fp += counts["fp"]
        fn += counts["fn"]
        exact += int(counts["exact_match"])
        any_hit += int(counts["tp"] > 0)

        precision = safe_div(counts["tp"], counts["tp"] + counts["fp"])
        recall = safe_div(counts["tp"], counts["tp"] + counts["fn"])
        per_precision.append(precision)
        per_recall.append(recall)
        per_f1.append(f1_score(precision, recall))

        gold = row.get("gold_categories", [])
        patterns = row.get("final_attack_patterns", [])
        total_gold += len(gold)
        for k in topk_micro_hits:
            hits = len(category_matches_for_patterns(patterns, gold, limit=k))
            topk_micro_hits[k] += hits
            topk_macro[k].append(safe_div(hits, len(gold)))

    micro_precision = safe_div(tp, tp + fp)
    micro_recall = safe_div(tp, tp + fn)
    return {
        "rows": len(rows),
        "exact_match": safe_div(exact, len(rows)),
        "exact_match_count": exact,
        "any_hit_accuracy": safe_div(any_hit, len(rows)),
        "any_hit_count": any_hit,
        "micro_precision": micro_precision,
        "micro_recall": micro_recall,
        "micro_f1": f1_score(micro_precision, micro_recall),
        "macro_precision": mean(per_precision) if per_precision else 0.0,
        "macro_recall": mean(per_recall) if per_recall else 0.0,
        "macro_f1": mean(per_f1) if per_f1 else 0.0,
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "topk_micro_recall": {f"recall@{k}": safe_div(v, total_gold) for k, v in topk_micro_hits.items()},
        "topk_macro_recall": {
            f"recall@{k}": mean(values) if values else 0.0 for k, values in topk_macro.items()
        },
    }


def latency_summary(rows):
    latencies = [row.get("latency_s", 0.0) for row in rows if not row.get("error") and row.get("latency_s")]
    if not latencies:
        return {"avg_s": 0.0, "median_s": 0.0, "min_s": 0.0, "max_s": 0.0}
    ordered = sorted(latencies)
    p95_index = min(len(ordered) - 1, int(0.95 * (len(ordered) - 1)))
    return {
        "avg_s": mean(latencies),
        "median_s": median(latencies),
        "min_s": min(latencies),
        "max_s": max(latencies),
        "p95_s": ordered[p95_index],
    }


def build_summary(rows):
    successful = [row for row in rows if not row.get("error")]
    errors = [row for row in rows if row.get("error")]
    invalid = [row for row in rows if (row.get("validation") or {}).get("invalid_output")]
    parse_errors = [row for row in rows if (row.get("validation") or {}).get("parse_error")]
    repaired = [row for row in rows if (row.get("validation") or {}).get("repair_applied")]
    non_empty = [row for row in successful if row.get("predicted_attack_ids")]

    return {
        "total_rows": len(rows),
        "successful_rows": len(successful),
        "request_error_rows": len(errors),
        "non_empty_prediction_rows": len(non_empty),
        "repaired_output_rows": len(repaired),
        "coverage_success_rate": safe_div(len(successful), len(rows)),
        "coverage_non_empty_rate": safe_div(len(non_empty), len(rows)),
        "invalid_output_rate_all": safe_div(len(invalid), len(rows)),
        "parse_error_rate_all": safe_div(len(parse_errors), len(rows)),
        "repaired_output_rate_all": safe_div(len(repaired), len(rows)),
        "latency": latency_summary(successful),
        "overall_including_errors": aggregate(rows),
        "successful_only": aggregate(successful),
    }


def write_error_analysis(rows, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "cve_id",
                "error",
                "gold_categories",
                "predicted_attack_ids",
                "matched_categories",
                "false_negative_categories",
                "false_positive_predicted_ids",
                "parse_error",
                "invalid_output",
                "repair_applied",
                "repair_method",
                "latency_s",
            ],
        )
        writer.writeheader()
        for row in rows:
            counts = row_counts(row)
            validation = row.get("validation") or {}
            writer.writerow(
                {
                    "cve_id": row.get("cve_id", ""),
                    "error": row.get("error") or "",
                    "gold_categories": "; ".join(row.get("gold_categories", [])),
                    "predicted_attack_ids": "; ".join(row.get("predicted_attack_ids", [])),
                    "matched_categories": "; ".join(counts["matched"]),
                    "false_negative_categories": "; ".join(counts["false_negatives"]),
                    "false_positive_predicted_ids": "; ".join(counts["false_positive_ids"]),
                    "parse_error": validation.get("parse_error") or "",
                    "invalid_output": validation.get("invalid_output", False),
                    "repair_applied": validation.get("repair_applied", False),
                    "repair_method": validation.get("repair_method") or "",
                    "latency_s": row.get("latency_s", 0.0),
                }
            )


def write_summary_csv(summary, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for scope in ["overall_including_errors", "successful_only"]:
        metrics = summary[scope]
        rows.append(
            {
                "scope": scope,
                "rows": metrics["rows"],
                "exact_match": metrics["exact_match"],
                "any_hit_accuracy": metrics["any_hit_accuracy"],
                "micro_precision": metrics["micro_precision"],
                "micro_recall": metrics["micro_recall"],
                "micro_f1": metrics["micro_f1"],
                "macro_precision": metrics["macro_precision"],
                "macro_recall": metrics["macro_recall"],
                "macro_f1": metrics["macro_f1"],
                "recall@1_micro": metrics["topk_micro_recall"]["recall@1"],
                "recall@3_micro": metrics["topk_micro_recall"]["recall@3"],
                "recall@5_micro": metrics["topk_micro_recall"]["recall@5"],
            }
        )
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description="Valuta predizioni CVE2ATT&CK a livello categoria/nome.")
    parser.add_argument("--predictions", type=Path, default=DEFAULT_PREDICTIONS)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()

    rows = read_jsonl(args.predictions)
    output_dir = args.output_dir or args.predictions.parent
    summary = build_summary(rows)

    summary_json = output_dir / "metrics_summary.json"
    summary_csv = output_dir / "metrics_summary.csv"
    error_csv = output_dir / "error_analysis.csv"
    with summary_json.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, ensure_ascii=False, sort_keys=True)
    write_summary_csv(summary, summary_csv)
    write_error_analysis(rows, error_csv)

    print(json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True))
    print(f"Summary JSON: {summary_json}")
    print(f"Summary CSV: {summary_csv}")
    print(f"Error analysis: {error_csv}")


if __name__ == "__main__":
    main()
