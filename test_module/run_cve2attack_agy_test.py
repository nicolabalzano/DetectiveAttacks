#!/usr/bin/env python3
"""
Run the CVE2ATT&CK prompt benchmark via `agy` (Antigravity CLI).

Uses the same 100-CVE dataset and prompt structure as run_cve2attack_prompt_test.py,
but invokes `agy -p -` (stdin) instead of the NVIDIA NIM API.
Output is fully compatible with evaluate_cve2attack_predictions.py.

Usage:
    python run_cve2attack_agy_test.py
    python run_cve2attack_agy_test.py --sample-size 10
    python run_cve2attack_agy_test.py --description-chars 200    # shorter prompt (~53K tokens)
    python run_cve2attack_agy_test.py --description-chars 500    # same as NIM test (~104K tokens)
    python run_cve2attack_agy_test.py --resume                   # skip already-completed CVEs

Prompt size reference (691 Enterprise ATT&CK candidates):
    --description-chars   0  =>  ~67K chars  (~17K tokens)
    --description-chars  50  => ~110K chars  (~28K tokens)
    --description-chars 100  => ~145K chars  (~36K tokens)
    --description-chars 200  => ~214K chars  (~53K tokens)   <-- default
    --description-chars 500  => ~418K chars  (~104K tokens)  <-- same as NIM test
    --full-descriptions      => ~936K chars  (~234K tokens)
"""

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

from attack_catalog import attack_pattern_index, load_enterprise_attack_patterns
from cve2attack_dataset import DEFAULT_DATASET_DIR, load_cve2attack, write_csv, write_jsonl
from llm_output_validation import validate_attack_ids

TEST_MODULE_DIR = Path(__file__).resolve().parent
DEFAULT_OUTPUT_DIR = TEST_MODULE_DIR / "results" / "agy_gemini"
DEFAULT_TRACE_DIR = TEST_MODULE_DIR / "logs" / "agy_gemini"

MODEL_NAME = "gemini-3.5-flash-high"


def log_progress(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}", flush=True)


def build_prompt_text(candidates, vuln_description, description_chars=200):
    """
    Build the full prompt text for agy.

    Mirrors the two-message structure from run_cve2attack_prompt_test.py
    (system + user), collapsed into a single text prompt for `agy -p`.
    The vulnerability description is placed BEFORE the ATT&CK catalog so
    that if any truncation occurs, the CVE context is preserved.
    """
    system_part = (
        "Reasoning mode: off. Do not think step by step in the response. "
        "Do not expose intermediate reasoning. "
        "Return only the final JSON array requested by the instructions. "
        "You are an Expert Threat Intelligence Analyst specializing in mapping "
        "vulnerabilities to MITRE ATT&CK patterns. Your task is to identify the "
        "most relevant attack patterns from the provided list that correspond to "
        "a given vulnerability description. You must ONLY use the attack patterns "
        "provided below."
    )

    user_part = (
        f"Task: Map the following vulnerability description to the provided Attack Patterns.\n"
        f"Vulnerability Description:\n{vuln_description}\n\n"
        f"Requirement: Identify the Attack Pattern IDs that represent the techniques "
        f"used to exploit this vulnerability or the consequences of its exploitation.\n"
        f'Output: A JSON list of strings containing ONLY the IDs.\n'
        f'Example: ["T1001", "T1002"]'
    )

    catalog_part = " Each pattern is described by its ID, Name, and Description:"
    for pattern in candidates:
        catalog_part += " " + pattern.as_candidate_text(description_chars=description_chars)

    instructions_part = (
        "\n\nINSTRUCTIONS:\n"
        "1. Analyze the vulnerability description provided above.\n"
        "2. Compare it against the descriptions of the attack patterns provided.\n"
        "3. Identify the attack patterns that best describe the exploitation method "
        "or impact of the vulnerability.\n"
        "4. Return ONLY a JSON array containing the IDs of the matching attack patterns.\n"
        "5. Do not include any explanation or extra text.\n"
        '6. Format: ["ID1", "ID2", ...]. Example: ["T1609", "T1612"].\n'
        "7. If no perfect match is found, select the most semantically relevant ones.\n"
    )

    return f"{system_part}\n\n{user_part}\n\n{catalog_part}\n{instructions_part}"


def call_agy(prompt_text, print_timeout="5m"):
    """
    Invoke `agy -p -` with the prompt piped via stdin to avoid
    OS ARG_MAX limits.
    """
    started_at = time.perf_counter()
    try:
        result = subprocess.run(
            ["agy", "-p", "-", "--print-timeout", print_timeout,
             "--dangerously-skip-permissions"],
            input=prompt_text,
            capture_output=True,
            text=True,
            timeout=600,  # hard 10-minute wall-clock timeout
        )
        latency_s = time.perf_counter() - started_at
        if result.returncode != 0:
            error_msg = (result.stderr or "").strip()[:500]
            return "", latency_s, f"agy exit code {result.returncode}: {error_msg}"
        raw_output = result.stdout.strip()
        return raw_output, latency_s, None
    except subprocess.TimeoutExpired:
        latency_s = time.perf_counter() - started_at
        return "", latency_s, f"agy timed out after {latency_s:.1f}s"
    except Exception as exc:
        latency_s = time.perf_counter() - started_at
        return "", latency_s, repr(exc)


def compare_categories_to_predictions(gold_categories, predicted_patterns):
    """Same logic as run_cve2attack_prompt_test.py."""
    gold_lower = {cat.lower(): cat for cat in gold_categories}
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

    unmatched_gold = [cat for cat in gold_categories if cat not in matched]
    return {
        "matched_gold_categories_by_name": matched,
        "unmatched_gold_categories": unmatched_gold,
        "predicted_ids_not_matching_gold_category_names": unmatched_predicted_ids,
    }


def technique_summary(patterns):
    return [
        {
            "attack_id": p.attack_id,
            "name": p.name,
            "tactics": list(p.tactics),
            "parent_id": p.parent_id,
            "parent_name": p.parent_name,
            "is_subtechnique": p.is_subtechnique,
        }
        for p in patterns
    ]


def dump_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False, sort_keys=True)


def _prediction_record(trace, trace_path):
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


def _build_error_trace(model, cve_id, item, error, candidate_count):
    return {
        "model": model,
        "cve_id": cve_id,
        "splits": item["splits"],
        "description": item["description"],
        "gold_categories": item["gold_categories"],
        "domain": "Enterprise",
        "domain_forced": True,
        "candidate_count": candidate_count,
        "error": error,
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


def detect_agy_model():
    """
    Read the model currently selected in agy from ~/.gemini/antigravity-cli/settings.json.
    Returns a clean slug like 'gemini-3.5-flash-high' or the raw name if not matched.
    """
    settings_path = Path.home() / ".gemini" / "antigravity-cli" / "settings.json"
    if settings_path.exists():
        try:
            with settings_path.open(encoding="utf-8") as f:
                settings = json.load(f)
            raw_model = settings.get("model", "")
            if raw_model:
                model_str = raw_model.lower()
                # Human readable settings names -> clean slugs
                if "gemini 3.5 flash (high)" in model_str or "gemini-3.5-flash-high" in model_str:
                    return "gemini-3.5-flash-high"
                elif "gemini 3.5 flash (medium)" in model_str or "gemini-3.5-flash-medium" in model_str:
                    return "gemini-3.5-flash-medium"
                elif "gemini 3.5 flash (low)" in model_str or "gemini-3.5-flash-low" in model_str:
                    return "gemini-3.5-flash-low"
                elif "gemini 2.5 flash (high)" in model_str:
                    return "gemini-2.5-flash-high"
                elif "gemini 2.5 flash (medium)" in model_str:
                    return "gemini-2.5-flash-medium"
                elif "gemini 2.5 flash (low)" in model_str:
                    return "gemini-2.5-flash-low"
                clean_name = raw_model.replace(" ", "-").replace("(", "").replace(")", "").lower()
                return clean_name
        except Exception:
            pass
    return "gemini-3.5-flash-high" # Default fallback


def main():
    detected_model = detect_agy_model()
    
    parser = argparse.ArgumentParser(
        description="Run CVE2ATT&CK prompt benchmark via agy (Antigravity CLI)."
    )
    parser.add_argument("--dataset-dir", type=Path, default=DEFAULT_DATASET_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--trace-dir", type=Path, default=DEFAULT_TRACE_DIR)
    parser.add_argument("--sample-size", type=int, default=None,
                        help="Limit to N CVEs (for quick tests).")
    parser.add_argument("--offset", type=int, default=0,
                        help="Skip the first N CVEs.")
    parser.add_argument("--description-chars", type=int, default=200,
                        help="Max chars per ATT&CK technique description in prompt (default: 200, ~53K tokens).")
    parser.add_argument("--full-descriptions", action="store_true",
                        help="Use full ATT&CK descriptions (no truncation).")
    parser.add_argument("--print-timeout", default="5m",
                        help="Timeout for each agy -p call (default: 5m).")
    parser.add_argument("--resume", action="store_true",
                        help="Skip CVEs that already have a valid trace file without errors or empty outputs.")
    parser.add_argument("--delay", type=float, default=6.0,
                        help="Delay in seconds between API calls to prevent rate limits (default: 6.0).")
    parser.add_argument("--parent-only", action="store_true",
                        help="Use only parent techniques (no sub-techniques).")
    parser.add_argument("--use-extended-train", action="store_true",
                        help="Use final_extended_X/y_train.csv instead of original train split.")
    parser.add_argument("--model-name", default=detected_model,
                        help=f"Model name label for output files (default auto-detected: {detected_model}).")
    args = parser.parse_args()

    if args.full_descriptions:
        args.description_chars = None

    # --- Load dataset (same 100 CVEs as NIM test) ---
    dataset_rows = load_cve2attack(args.dataset_dir, use_extended_train=args.use_extended_train)
    if args.offset:
        dataset_rows = dataset_rows[args.offset:]
    if args.sample_size:
        dataset_rows = dataset_rows[:args.sample_size]

    output_dir = args.output_dir
    trace_dir = args.trace_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    trace_dir.mkdir(parents=True, exist_ok=True)

    # Save the dataset selection
    write_jsonl(dataset_rows, output_dir / "cve2attack_selected.jsonl")
    write_csv(dataset_rows, output_dir / "cve2attack_selected.csv")

    # --- Load ATT&CK catalog (same as NIM test) ---
    candidates = load_enterprise_attack_patterns(include_subtechniques=not args.parent_only)
    index = attack_pattern_index(candidates)
    valid_ids = set(index)
    catalog_path = output_dir / "enterprise_attack_candidates.json"
    dump_json(catalog_path, [p.as_dict() for p in candidates])

    slug = args.model_name.replace(".", "_").replace("-", "_").replace("/", "_")
    jsonl_path = output_dir / f"predictions_{slug}.jsonl"
    trace_model_dir = trace_dir / slug
    trace_model_dir.mkdir(parents=True, exist_ok=True)

    # Show a sample prompt size
    sample_prompt = build_prompt_text(candidates, "sample", description_chars=args.description_chars)
    print(f"{'='*50}")
    print(f"  Model (Selected): {args.model_name}")
    print(f"  CVEs:             {len(dataset_rows)}")
    print(f"  ATT&CK candidates: {len(candidates)}")
    print(f"  Desc chars:       {args.description_chars or 'full'}")
    print(f"  Prompt size:      ~{len(sample_prompt):,} chars (~{len(sample_prompt)//4:,} tokens)")
    print(f"  Output JSONL:     {jsonl_path}")
    print(f"  Resume Mode:      {args.resume}")
    print(f"  Delay between:    {args.delay}s")
    print(f"{'='*50}")
    confirm = input("\nConfermi? (y/N): ").strip().lower()
    if confirm not in ("y", "yes", "s", "si", "sì"):
        print("Annullato.")
        sys.exit(0)
    print()

    # --- Run benchmark ---
    with jsonl_path.open("w", encoding="utf-8") as jsonl_handle:
        for count, item in enumerate(dataset_rows, start=1):
            cve_id = item["cve_id"]
            trace_path = trace_model_dir / f"{cve_id}.json"

            # Resume: skip if trace already exists and has no error or empty/corrupt outputs
            if args.resume and trace_path.exists():
                try:
                    with trace_path.open(encoding="utf-8") as f:
                        existing_trace = json.load(f)
                    
                    val = existing_trace.get("validation", {})
                    is_valid = (
                        not existing_trace.get("error") and
                        existing_trace.get("raw_model_output") and
                        val.get("parse_error") != "non_json" and
                        not val.get("invalid_output")
                    )
                    
                    if is_valid:
                        record = _prediction_record(existing_trace, trace_path)
                        jsonl_handle.write(
                            json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n"
                        )
                        jsonl_handle.flush()
                        log_progress(
                            f"[{args.model_name}] {count}/{len(dataset_rows)} "
                            f"{cve_id}: resumed from cache"
                        )
                        continue
                except (json.JSONDecodeError, KeyError):
                    pass  # re-run this CVE

            # Build prompt
            prompt_text = build_prompt_text(
                candidates, item["description"], description_chars=args.description_chars
            )

            log_progress(
                f"[{args.model_name}] {count}/{len(dataset_rows)} {cve_id}: "
                f"calling agy ({len(prompt_text):,} chars)"
            )

            # Call agy
            raw_output, latency_s, error = call_agy(prompt_text, args.print_timeout)

            if error:
                trace = _build_error_trace(
                    args.model_name, cve_id, item, error, len(candidates)
                )
                trace["latency_s"] = latency_s
                dump_json(trace_path, trace)
                record = _prediction_record(trace, trace_path)
                jsonl_handle.write(
                    json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n"
                )
                jsonl_handle.flush()
                log_progress(
                    f"[{args.model_name}] {count}/{len(dataset_rows)} {cve_id}: "
                    f"ERROR ({latency_s:.1f}s) {error[:200]}"
                )
                
                # Still sleep if error occurs, to be nice to the API
                if count < len(dataset_rows) and args.delay > 0:
                    time.sleep(args.delay)
                continue

            # Validate output
            validation = validate_attack_ids(raw_output, valid_ids)
            predicted_patterns = [index[aid] for aid in validation["final_ids"]]
            category_comparison = compare_categories_to_predictions(
                item["gold_categories"], predicted_patterns
            )

            trace = {
                "model": args.model_name,
                "cve_id": cve_id,
                "splits": item["splits"],
                "description": item["description"],
                "gold_categories": item["gold_categories"],
                "domain": "Enterprise",
                "domain_forced": True,
                "candidate_count": len(candidates),
                "candidate_description_chars": args.description_chars,
                "raw_model_output": raw_output,
                "validation": validation,
                "final_attack_patterns": technique_summary(predicted_patterns),
                "category_comparison": category_comparison,
                "latency_s": latency_s,
            }
            dump_json(trace_path, trace)

            record = _prediction_record(trace, trace_path)
            jsonl_handle.write(
                json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n"
            )
            jsonl_handle.flush()

            log_progress(
                f"[{args.model_name}] {count}/{len(dataset_rows)} {cve_id}: "
                f"done ({latency_s:.1f}s, ids={validation['final_ids']}, "
                f"parse_error={validation['parse_error']}, "
                f"invalid={validation['invalid_output']})"
            )

            # Sleep to avoid rate limiting
            if count < len(dataset_rows) and args.delay > 0:
                time.sleep(args.delay)

    # --- Summary ---
    summary_path = output_dir / "run_summary.json"
    dump_json(summary_path, {
        "model": args.model_name,
        "description_chars": args.description_chars,
        "jsonl": str(jsonl_path),
        "rows": len(dataset_rows),
    })
    print(f"\nDone. Predictions: {jsonl_path}")
    print(f"Summary: {summary_path}")
    print(f"\nTo evaluate, run:")
    print(f"  python evaluate_cve2attack_predictions.py --predictions {jsonl_path}")


if __name__ == "__main__":
    main()

