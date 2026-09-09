import json
import re

from attack_catalog import ATTACK_ID_RE


def parse_json_list(raw_output):
    text = (raw_output or "").strip()
    text = re.sub(r"^```(?:json)?", "", text, flags=re.IGNORECASE).strip()
    text = re.sub(r"```$", "", text).strip()

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\[[\s\S]*\]", text)
        if not match:
            return None, "non_json"
        try:
            parsed = json.loads(match.group(0))
        except json.JSONDecodeError:
            return None, "non_json"

    if not isinstance(parsed, list):
        return None, "not_list"
    if not all(isinstance(item, str) for item in parsed):
        return None, "non_string_items"
    return parsed, None


def parse_truncated_json_list(raw_output):
    text = (raw_output or "").strip()
    text = re.sub(r"^```(?:json)?", "", text, flags=re.IGNORECASE).strip()
    text = re.sub(r"```$", "", text).strip()
    if not text.startswith("["):
        return None

    repaired_ids = []
    seen = set()
    for match in re.finditer(r"T\d{4}(?:\.\d{3})?", text.upper()):
        # Do not turn a truncated sub-technique such as "T1552." into parent T1552.
        if match.end() < len(text) and text[match.end()] == ".":
            continue
        attack_id = match.group(0)
        if attack_id not in seen:
            seen.add(attack_id)
            repaired_ids.append(attack_id)
    return repaired_ids or None


def validate_attack_ids(raw_output, valid_ids, allow_repair=True):
    parsed, parse_error = parse_json_list(raw_output)
    repair_applied = False
    repair_method = None
    original_parse_error = None

    if parse_error and allow_repair:
        repaired = parse_truncated_json_list(raw_output)
        if repaired:
            parsed = repaired
            original_parse_error = parse_error
            parse_error = None
            repair_applied = True
            repair_method = "truncated_json_array_id_extraction"

    if parse_error:
        return {
            "final_ids": [],
            "raw_ids": [],
            "invalid_ids": [],
            "duplicate_ids": [],
            "malformed_ids": [],
            "parse_error": parse_error,
            "invalid_output": True,
            "repair_applied": False,
            "repair_method": None,
            "original_parse_error": None,
        }

    final_ids = []
    duplicate_ids = []
    invalid_ids = []
    malformed_ids = []
    seen = set()
    for item in parsed:
        attack_id = item.strip().upper().replace("/", ".")
        if not ATTACK_ID_RE.match(attack_id):
            malformed_ids.append(item)
            continue
        if attack_id not in valid_ids:
            invalid_ids.append(attack_id)
            continue
        if attack_id in seen:
            duplicate_ids.append(attack_id)
            continue
        seen.add(attack_id)
        final_ids.append(attack_id)

    return {
        "final_ids": final_ids,
        "raw_ids": parsed,
        "invalid_ids": invalid_ids,
        "duplicate_ids": duplicate_ids,
        "malformed_ids": malformed_ids,
        "parse_error": None,
        "invalid_output": bool(invalid_ids or malformed_ids),
        "repair_applied": repair_applied,
        "repair_method": repair_method,
        "original_parse_error": original_parse_error,
    }
