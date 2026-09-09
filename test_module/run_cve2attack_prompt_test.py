import argparse
import csv
import json
import shutil
import sys
import time
from pathlib import Path

from attack_catalog import attack_pattern_index, load_enterprise_attack_patterns
from cve2attack_dataset import DEFAULT_DATASET_DIR, load_cve2attack, write_csv, write_jsonl
from llm_output_validation import validate_attack_ids
from nvidia_nim_api import NvidiaNIMPromptAPI, dump_json, model_slug, parse_models


TEST_MODULE_DIR = Path(__file__).resolve().parent
DEFAULT_OUTPUT_DIR = TEST_MODULE_DIR / "results"
DEFAULT_TRACE_DIR = TEST_MODULE_DIR / "logs"

DOMAIN_NAMES = {
    "enterprise": "Enterprise",
    "ics": "Industrial Control System",
    "mobile": "Mobile",
    "atlas": "Adversarial Machine Learning",
}

DOMAIN_TO_MITRE = {
    "Enterprise": "enterprise-attack",
    "Industrial Control System": "ics-attack",
    "Mobile": "mobile-attack",
    "Adversarial Machine Learning": "atlas",
}


def log_progress(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}", flush=True)


def build_mapping_messages(candidates, description_chars=500):
    system_content = (
        "Reasoning mode: off. Do not think step by step in the response. Do not expose intermediate reasoning. "
        "Return only the final JSON array requested by the instructions. "
        "You are an Expert Threat Intelligence Analyst specializing in mapping vulnerabilities to MITRE ATT&CK "
        "patterns. Your task is to identify the most relevant attack patterns from the provided list that correspond "
        "to a given vulnerability description. You must ONLY use the attack patterns provided below. Each pattern is "
        "described by its ID, Name, and Description:"
    )
    for pattern in candidates:
        system_content += " " + pattern.as_candidate_text(description_chars=description_chars)

    system_content += (
        """
            INSTRUCTIONS:
            1. Analyze the vulnerability description provided by the user.
            2. Compare it against the descriptions of the attack patterns provided above.
            3. Identify the attack patterns that best describe the exploitation method or impact of the vulnerability.
            4. Return ONLY a JSON array containing the IDs of the matching attack patterns.
            5. Do not include any explanation or extra text.
            6. Format: ["ID1", "ID2", ...]. Example: ["T1609", "T1612"].
            7. If no perfect match is found, select the most semantically relevant ones.
            """
    )
    return [{"role": "system", "content": system_content}]


def compare_categories_to_predictions(gold_categories, predicted_patterns):
    gold_lower = {category.lower(): category for category in gold_categories}
    matched = []
    unmatched_predicted_ids = []

    for pattern in predicted_patterns:
        names_to_check = [pattern.name]
        if pattern.parent_name:
            names_to_check.append(pattern.parent_name)
        if any(name.lower() in gold_lower for name in names_to_check):
            for name in names_to_check:
                if name.lower() in gold_lower and gold_lower[name.lower()] not in matched:
                    matched.append(gold_lower[name.lower()])
        else:
            unmatched_predicted_ids.append(pattern.attack_id)

    unmatched_gold = [category for category in gold_categories if category not in matched]
    return {
        "matched_gold_categories_by_name": matched,
        "unmatched_gold_categories": unmatched_gold,
        "predicted_ids_not_matching_gold_category_names": unmatched_predicted_ids,
    }


def technique_summary(patterns):
    return [
        {
            "attack_id": pattern.attack_id,
            "name": pattern.name,
            "tactics": list(pattern.tactics),
            "parent_id": pattern.parent_id,
            "parent_name": pattern.parent_name,
            "is_subtechnique": pattern.is_subtechnique,
        }
        for pattern in patterns
    ]


def write_rows_csv(rows, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "model",
        "cve_id",
        "splits",
        "gold_categories",
        "predicted_attack_ids",
        "predicted_attack_names",
        "predicted_tactics",
        "matched_gold_categories_by_name",
        "unmatched_gold_categories",
        "predicted_ids_not_matching_gold_category_names",
        "invalid_ids",
        "malformed_ids",
        "duplicate_ids",
        "parse_error",
        "latency_s",
        "trace_path",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def backup_once(path, suffix):
    backup_path = path.with_name(path.name + suffix)
    if path.exists() and not backup_path.exists():
        shutil.copy2(path, backup_path)
    return backup_path


def row_from_trace(trace, trace_path):
    predicted_patterns = trace.get("final_attack_patterns", [])
    validation = trace.get("validation", {})
    category_comparison = trace.get("category_comparison", {})
    return {
        "model": trace.get("model", ""),
        "cve_id": trace.get("cve_id", ""),
        "splits": "; ".join(trace.get("splits", [])),
        "gold_categories": "; ".join(trace.get("gold_categories", [])),
        "predicted_attack_ids": "; ".join(validation.get("final_ids", [])),
        "predicted_attack_names": "; ".join(pattern.get("name", "") for pattern in predicted_patterns),
        "predicted_tactics": "; ".join(
            f"{pattern.get('attack_id', '')}:{','.join(pattern.get('tactics', []))}"
            for pattern in predicted_patterns
        ),
        "matched_gold_categories_by_name": "; ".join(
            category_comparison.get("matched_gold_categories_by_name", [])
        ),
        "unmatched_gold_categories": "; ".join(category_comparison.get("unmatched_gold_categories", [])),
        "predicted_ids_not_matching_gold_category_names": "; ".join(
            category_comparison.get("predicted_ids_not_matching_gold_category_names", [])
        ),
        "invalid_ids": "; ".join(validation.get("invalid_ids", [])),
        "malformed_ids": "; ".join(validation.get("malformed_ids", [])),
        "duplicate_ids": "; ".join(validation.get("duplicate_ids", [])),
        "parse_error": validation.get("parse_error") or "",
        "latency_s": f"{trace.get('latency_s', 0.0):.3f}",
        "trace_path": str(trace_path),
    }


def prediction_record_from_trace(trace, trace_path):
    return {
        "model": trace.get("model", ""),
        "cve_id": trace.get("cve_id", ""),
        "splits": trace.get("splits", []),
        "description": trace.get("description", ""),
        "gold_categories": trace.get("gold_categories", []),
        "predicted_attack_ids": trace.get("validation", {}).get("final_ids", []),
        "final_attack_patterns": trace.get("final_attack_patterns", []),
        "category_comparison": trace.get("category_comparison", {}),
        "validation": trace.get("validation", {}),
        "latency_s": trace.get("latency_s", 0.0),
        "trace_path": str(trace_path),
        "error": trace.get("error"),
    }


def run_model(
    model,
    dataset_rows,
    candidates,
    output_dir,
    trace_dir,
    dry_run=False,
    description_chars=500,
    resume=True,
    retry_invalid=False,
    sleep_s=0.0,
):
    index = attack_pattern_index(candidates)
    valid_ids = set(index)
    api = None if dry_run else NvidiaNIMPromptAPI(model=model)
    slug = model_slug(model)

    result_rows = []
    jsonl_path = output_dir / f"predictions_{slug}.jsonl"
    trace_model_dir = trace_dir / slug
    jsonl_path.parent.mkdir(parents=True, exist_ok=True)
    trace_model_dir.mkdir(parents=True, exist_ok=True)

    with jsonl_path.open("w", encoding="utf-8") as jsonl_handle:
        for count, item in enumerate(dataset_rows, start=1):
            cve_id = item["cve_id"]
            trace_path = trace_model_dir / f"{cve_id}.json"

            if resume and trace_path.exists():
                with trace_path.open(encoding="utf-8") as handle:
                    trace = json.load(handle)
                if not trace.get("error"):
                    validation = trace.get("validation") or {}
                    raw_output = trace.get("raw_model_output", "")
                    already_retried = trace_path.with_name(trace_path.name + ".before_retry").exists()
                    retry_existing_trace = (
                        (validation.get("invalid_output") and bool(raw_output.strip()))
                        or validation.get("repair_applied")
                        or bool(trace.get("validation_before_repair"))
                    )
                    if retry_invalid and retry_existing_trace and not already_retried:
                        backup_path = backup_once(trace_path, ".before_retry")
                        log_progress(
                            f"[{model}] {count}/{len(dataset_rows)} {cve_id}: retrying malformed output "
                            f"(backup={backup_path})"
                        )
                    else:
                        jsonl_handle.write(
                            json.dumps(
                                prediction_record_from_trace(trace, trace_path),
                                ensure_ascii=False,
                                sort_keys=True,
                            )
                            + "\n"
                        )
                        jsonl_handle.flush()
                        result_rows.append(row_from_trace(trace, trace_path))
                        log_progress(f"[{model}] {count}/{len(dataset_rows)} {cve_id}: resumed from {trace_path}")
                        continue
                else:
                    if retry_invalid:
                        backup_path = backup_once(trace_path, ".before_retry")
                        log_progress(
                            f"[{model}] {count}/{len(dataset_rows)} {cve_id}: retrying previous error "
                            f"(backup={backup_path})"
                        )
                    else:
                        log_progress(f"[{model}] {count}/{len(dataset_rows)} {cve_id}: retrying previous error")

            mapping_messages = build_mapping_messages(candidates, description_chars=description_chars)
            candidate_ids = [pattern.attack_id for pattern in candidates]
            candidate_count = len(candidate_ids)
            prompt_chars = sum(len(message["content"]) for message in mapping_messages) + len(item["description"])
            log_progress(
                f"[{model}] {count}/{len(dataset_rows)} {cve_id}: starting request "
                f"(candidates={candidate_count}, prompt_chars~{prompt_chars}, "
                f"description_chars={description_chars if description_chars is not None else 'full'})"
            )

            if dry_run:
                raw_output = "[]"
                response_json = {"dry_run": True}
                latency_s = 0.0
            else:
                try:
                    raw_output, request_messages, response_json, latency_s = api.get_at_related_from_query(
                        mapping_messages, item["description"]
                    )
                    mapping_messages = request_messages
                except Exception as exc:
                    trace = {
                        "model": model,
                        "cve_id": cve_id,
                        "splits": item["splits"],
                        "description": item["description"],
                        "gold_categories": item["gold_categories"],
                        "domain": "Enterprise",
                        "domain_forced": True,
                        "candidate_count": candidate_count,
                        "candidate_ids": candidate_ids,
                        "prompt_messages": mapping_messages,
                        "error": repr(exc),
                        "validation": {
                            "final_ids": [],
                            "raw_ids": [],
                            "invalid_ids": [],
                            "duplicate_ids": [],
                            "malformed_ids": [],
                            "parse_error": "request_error",
                            "invalid_output": True,
                        },
                        "final_attack_patterns": [],
                        "category_comparison": {
                            "matched_gold_categories_by_name": [],
                            "unmatched_gold_categories": item["gold_categories"],
                            "predicted_ids_not_matching_gold_category_names": [],
                        },
                        "latency_s": 0.0,
                    }
                    dump_json(trace_path, trace)
                    jsonl_handle.write(
                        json.dumps(prediction_record_from_trace(trace, trace_path), ensure_ascii=False, sort_keys=True)
                        + "\n"
                    )
                    jsonl_handle.flush()
                    result_rows.append(row_from_trace(trace, trace_path))
                    log_progress(f"[{model}] {count}/{len(dataset_rows)} {cve_id}: ERROR {exc}")
                    if sleep_s:
                        time.sleep(sleep_s)
                    continue

            validation = validate_attack_ids(raw_output, valid_ids)
            predicted_patterns = [index[attack_id] for attack_id in validation["final_ids"]]
            category_comparison = compare_categories_to_predictions(item["gold_categories"], predicted_patterns)
            trace = {
                "model": model,
                "cve_id": cve_id,
                "splits": item["splits"],
                "description": item["description"],
                "gold_categories": item["gold_categories"],
                "domain": "Enterprise",
                "domain_forced": True,
                "candidate_count": candidate_count,
                "candidate_ids": candidate_ids,
                "candidate_description_chars": description_chars,
                "prompt_messages": mapping_messages,
                "raw_model_output": raw_output,
                "model_response_json": response_json,
                "validation": validation,
                "final_attack_patterns": technique_summary(predicted_patterns),
                "category_comparison": category_comparison,
                "latency_s": latency_s,
            }
            dump_json(trace_path, trace)

            prediction_record = {
                "model": model,
                "cve_id": cve_id,
                "splits": item["splits"],
                "description": item["description"],
                "gold_categories": item["gold_categories"],
                "predicted_attack_ids": validation["final_ids"],
                "final_attack_patterns": technique_summary(predicted_patterns),
                "category_comparison": category_comparison,
                "validation": validation,
                "latency_s": latency_s,
                "trace_path": str(trace_path),
            }
            jsonl_handle.write(json.dumps(prediction_record, ensure_ascii=False, sort_keys=True) + "\n")
            jsonl_handle.flush()

            result_rows.append(
                {
                    "model": model,
                    "cve_id": cve_id,
                    "splits": "; ".join(item["splits"]),
                    "gold_categories": "; ".join(item["gold_categories"]),
                    "predicted_attack_ids": "; ".join(validation["final_ids"]),
                    "predicted_attack_names": "; ".join(pattern.name for pattern in predicted_patterns),
                    "predicted_tactics": "; ".join(
                        f"{pattern.attack_id}:{','.join(pattern.tactics)}" for pattern in predicted_patterns
                    ),
                    "matched_gold_categories_by_name": "; ".join(
                        category_comparison["matched_gold_categories_by_name"]
                    ),
                    "unmatched_gold_categories": "; ".join(category_comparison["unmatched_gold_categories"]),
                    "predicted_ids_not_matching_gold_category_names": "; ".join(
                        category_comparison["predicted_ids_not_matching_gold_category_names"]
                    ),
                    "invalid_ids": "; ".join(validation["invalid_ids"]),
                    "malformed_ids": "; ".join(validation["malformed_ids"]),
                    "duplicate_ids": "; ".join(validation["duplicate_ids"]),
                    "parse_error": validation["parse_error"] or "",
                    "latency_s": f"{latency_s:.3f}",
                    "trace_path": str(trace_path),
                }
            )

            log_progress(
                f"[{model}] {count}/{len(dataset_rows)} {cve_id}: done "
                f"(latency={latency_s:.2f}s, final_ids={validation['final_ids']}, "
                f"parse_error={validation['parse_error']}, invalid={validation['invalid_output']})"
            )
            if sleep_s:
                time.sleep(sleep_s)

    csv_path = output_dir / f"manual_comparison_{slug}.csv"
    write_rows_csv(result_rows, csv_path)
    return {"jsonl": str(jsonl_path), "csv": str(csv_path), "rows": len(result_rows)}


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Esegue il prompt test su CVE2ATT&CK unificato. Il gold resta in categorie CVE2ATT&CK; "
            "l'output predetto resta in ID ATT&CK reali."
        )
    )
    parser.add_argument("--dataset-dir", type=Path, default=DEFAULT_DATASET_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--trace-dir", type=Path, default=DEFAULT_TRACE_DIR)
    parser.add_argument("--models", help="Lista modelli NVIDIA NIM separati da virgola.")
    parser.add_argument("--sample-size", type=int, default=None)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--description-chars", type=int, default=200)
    parser.add_argument(
        "--full-descriptions",
        action="store_true",
        help="Usa descrizioni ATT&CK complete nel prompt, senza taglio.",
    )
    parser.add_argument("--sleep", type=float, default=0.0, help="Pausa in secondi tra richieste API.")
    parser.add_argument("--no-resume", action="store_true", help="Non riusa trace già presenti.")
    parser.add_argument(
        "--retry-invalid",
        action="store_true",
        help=(
            "Rifà i trace esistenti con output malformato non vuoto, output riparato "
            "o errori precedenti. Gli output vuoti restano conteggiati come invalidi."
        ),
    )
    parser.add_argument(
        "--parent-only",
        action="store_true",
        help="Replica il filtro legacy di gptAPI.py usando solo tecniche parent, senza sub-technique.",
    )
    parser.add_argument(
        "--use-extended-train",
        action="store_true",
        help="Usa final_extended_X/y_train.csv invece dello split train originale.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Non chiama NVIDIA NIM: genera dataset, prompt trace e output vuoto per controllare il formato.",
    )
    args = parser.parse_args()

    if args.full_descriptions:
        args.description_chars = None

    dataset_rows = load_cve2attack(args.dataset_dir, use_extended_train=args.use_extended_train)
    if args.offset:
        dataset_rows = dataset_rows[args.offset :]
    if args.sample_size:
        dataset_rows = dataset_rows[: args.sample_size]

    output_dir = args.output_dir / "dry_run" if args.dry_run else args.output_dir
    trace_dir = args.trace_dir / "dry_run" if args.dry_run else args.trace_dir

    output_dir.mkdir(parents=True, exist_ok=True)
    trace_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(dataset_rows, output_dir / "cve2attack_selected.jsonl")
    write_csv(dataset_rows, output_dir / "cve2attack_selected.csv")

    candidates = load_enterprise_attack_patterns(include_subtechniques=not args.parent_only)
    catalog_path = output_dir / "enterprise_attack_candidates.json"
    dump_json(catalog_path, [pattern.as_dict() for pattern in candidates])

    print(f"CVEs loaded: {len(dataset_rows)}")
    print(f"Enterprise ATT&CK candidates: {len(candidates)}")
    print(f"Candidate catalog: {catalog_path}")

    summaries = []
    for model in parse_models(args.models):
        try:
            summaries.append(
                {
                    "model": model,
                    **run_model(
                        model=model,
                        dataset_rows=dataset_rows,
                        candidates=candidates,
                        output_dir=output_dir,
                        trace_dir=trace_dir,
                        dry_run=args.dry_run,
                        description_chars=args.description_chars,
                        resume=not args.no_resume,
                        retry_invalid=args.retry_invalid,
                        sleep_s=args.sleep,
                    ),
                }
            )
        except Exception as exc:
            print(f"ERROR running model {model}: {exc}", file=sys.stderr)
            if not args.dry_run:
                raise

    summary_path = output_dir / "run_summary.json"
    dump_json(summary_path, summaries)
    print(f"Summary: {summary_path}")


if __name__ == "__main__":
    main()
