import argparse
import json
import shutil
from pathlib import Path

from attack_catalog import attack_pattern_index, load_enterprise_attack_patterns
from llm_output_validation import validate_attack_ids
from run_cve2attack_prompt_test import (
    compare_categories_to_predictions,
    prediction_record_from_trace,
    row_from_trace,
    technique_summary,
    write_rows_csv,
)
from nvidia_nim_api import dump_json


def read_jsonl(path):
    with Path(path).open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def backup_once(path):
    backup = path.with_suffix(path.suffix + ".before_repair")
    if path.exists() and not backup.exists():
        shutil.copy2(path, backup)
    return backup


def repair_trace(trace, trace_path, index, valid_ids):
    old_validation = trace.get("validation") or {}
    raw_output = trace.get("raw_model_output", "")
    validation = validate_attack_ids(raw_output, valid_ids, allow_repair=True)
    predicted_patterns = [index[attack_id] for attack_id in validation["final_ids"]]

    if validation.get("repair_applied") and "validation_before_repair" not in trace:
        trace["validation_before_repair"] = old_validation

    trace["validation"] = validation
    trace["final_attack_patterns"] = technique_summary(predicted_patterns)
    trace["category_comparison"] = compare_categories_to_predictions(
        trace.get("gold_categories", []), predicted_patterns
    )
    dump_json(trace_path, trace)
    return trace


def main():
    parser = argparse.ArgumentParser(
        description="Ripara in modo conservativo output JSON troncati nei trace e rigenera JSONL/CSV."
    )
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--trace-dir", type=Path, required=True)
    parser.add_argument("--parent-only", action="store_true")
    args = parser.parse_args()

    candidates = load_enterprise_attack_patterns(include_subtechniques=not args.parent_only)
    index = attack_pattern_index(candidates)
    valid_ids = set(index)

    records = read_jsonl(args.predictions)
    repaired_count = 0
    still_invalid_count = 0
    rows = []
    output_records = []

    backup_once(args.predictions)
    csv_path = args.predictions.with_name(
        args.predictions.name.replace("predictions_", "manual_comparison_").replace(".jsonl", ".csv")
    )
    backup_once(csv_path)

    for record in records:
        trace_path = Path(record.get("trace_path") or "")
        if not trace_path.is_absolute():
            trace_path = Path.cwd() / trace_path
        if not trace_path.exists():
            trace_path = args.trace_dir / f"{record['cve_id']}.json"

        with trace_path.open(encoding="utf-8") as handle:
            trace = json.load(handle)

        old_validation = trace.get("validation") or {}
        trace = repair_trace(trace, trace_path, index, valid_ids)
        new_validation = trace.get("validation") or {}
        if new_validation.get("repair_applied") and not old_validation.get("repair_applied"):
            repaired_count += 1
        if new_validation.get("invalid_output"):
            still_invalid_count += 1

        output_records.append(prediction_record_from_trace(trace, trace_path))
        rows.append(row_from_trace(trace, trace_path))

    with args.predictions.open("w", encoding="utf-8") as handle:
        for record in output_records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    write_rows_csv(rows, csv_path)

    print(f"Predictions updated: {args.predictions}")
    print(f"Manual comparison updated: {csv_path}")
    print(f"Repaired traces: {repaired_count}")
    print(f"Still invalid after repair: {still_invalid_count}")


if __name__ == "__main__":
    main()
