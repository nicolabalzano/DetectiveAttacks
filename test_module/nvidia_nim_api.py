import json
import os
from pathlib import Path
import time

import requests
from requests import RequestException


NVIDIA_NIM_URL = "https://integrate.api.nvidia.com/v1/chat/completions"


def safe_response_text(response, limit=1500):
    try:
        return response.content[:limit].decode("utf-8", errors="replace")
    except Exception as exc:
        return f"<unable to decode response body: {exc!r}>"


class NvidiaNIMPromptAPI:
    """
    NVIDIA NIM adapter for the same prompt flow used by gptAPI.py:
    domain classification followed by vulnerability-to-attack-pattern mapping.
    """

    def __init__(self, model, api_key=None, timeout=180, temperature=0.0):
        load_env_file()
        self.model = model
        self.api_key = (
            api_key
            or os.getenv("NVIDIA_API_KEY")
            or os.getenv("NVIDIA_NIM_KEY")
            or os.getenv("NVIDIA_NIM_API_KEY")
            or os.getenv("NGC_API_KEY")
        )
        self.timeout = timeout
        self.temperature = temperature
        self.max_retries = int(os.getenv("NVIDIA_NIM_MAX_RETRIES", "20"))
        self.max_tokens = int(os.getenv("NVIDIA_NIM_MAX_TOKENS", "512"))
        self.url = os.getenv("NVIDIA_NIM_URL", NVIDIA_NIM_URL)
        if not self.api_key:
            raise ValueError("NVIDIA_API_KEY, NVIDIA_NIM_KEY, NVIDIA_NIM_API_KEY, or NGC_API_KEY not set")

    def make_request(self, messages):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

        started_at = time.perf_counter()
        retry_delay = 10
        last_error = None
        for attempt in range(self.max_retries):
            try:
                response = requests.post(self.url, headers=headers, json=payload, timeout=self.timeout)
            except RequestException as exc:
                last_error = repr(exc)
                if attempt == self.max_retries - 1:
                    latency_s = time.perf_counter() - started_at
                    raise RuntimeError(f"NVIDIA NIM request error after {latency_s:.1f}s: {last_error}")
                time.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, 120)
                continue

            latency_s = time.perf_counter() - started_at

            if response.status_code in (429, 500, 502, 503, 504):
                response_text = safe_response_text(response, 1500)
                last_error = f"HTTP {response.status_code}: {response_text[:500]}"
                if attempt == self.max_retries - 1:
                    raise RuntimeError(
                        f"NVIDIA NIM HTTP {response.status_code} after {latency_s:.1f}s: "
                        f"{response_text}"
                    )
                retry_after = response.headers.get("Retry-After")
                sleep_s = int(retry_after) if retry_after and retry_after.isdigit() else retry_delay
                time.sleep(max(sleep_s, retry_delay))
                retry_delay = min(retry_delay * 2, 120)
                continue

            if response.status_code >= 400:
                raise RuntimeError(f"NVIDIA NIM HTTP {response.status_code}: {safe_response_text(response)}")

            body = response.json()
            if isinstance(body, dict) and "error" in body:
                error = body.get("error") or {}
                code = error.get("code")
                last_error = f"NVIDIA NIM response error {code}: {json.dumps(error)[:500]}"
                if code in (429, 500, 502, 503, 504) and attempt < self.max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay = min(retry_delay * 2, 120)
                    continue
                raise RuntimeError(f"NVIDIA NIM response error after {latency_s:.1f}s: {json.dumps(error)[:1500]}")

            choices = body.get("choices") or []
            if not choices:
                last_error = f"NVIDIA NIM response without choices: {json.dumps(body)[:500]}"
                if attempt < self.max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay = min(retry_delay * 2, 120)
                    continue
                raise RuntimeError(f"{last_error[:1500]}")
            message = choices[0].get("message") or {}
            content = message.get("content")
            if content is None:
                content = message.get("reasoning") or ""
            return content, body, latency_s

        raise RuntimeError(f"NVIDIA NIM request failed unexpectedly: {last_error}")

    def get_domain_of_description(self, vuln_desc, list_of_domains):
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an Expert Cybersecurity Analyst. Your task is to classify a vulnerability "
                    "description into one of the following domains: "
                    + str(list(list_of_domains))
                    + """.\n\nINSTRUCTIONS:\n1. Analyze the provided vulnerability description.\n2. Determine which of the allowed domains best fits the context of the vulnerability.\n3. Return ONLY the domain name as a string.\n4. Do not include any extra text, punctuation, or explanation.\n5. If the domain is unclear, choose the most plausible one from the list.\n"""
                ),
            },
            {"role": "user", "content": "Classify this vulnerability description:\n" + vuln_desc},
        ]
        raw_output, response_json, latency_s = self.make_request(messages)
        return raw_output.strip().strip("'").strip('"'), messages, response_json, latency_s

    def get_at_related_from_query(self, messages, vuln_desc):
        request_messages = [dict(message) for message in messages]
        request_messages.append(
            {
                "role": "user",
                "content": (
                    """
                Task: Map the following vulnerability description to the provided Attack Patterns.
                Vulnerability Description:
                """
                    + vuln_desc
                    + """

                Requirement: Identify the Attack Pattern IDs that represent the techniques used to exploit this vulnerability or the consequences of its exploitation.
                Output: A JSON list of strings containing ONLY the IDs.
                Example: ["T1001", "T1002"]
                """
                ),
            }
        )
        raw_output, response_json, latency_s = self.make_request(request_messages)
        return raw_output, request_messages, response_json, latency_s


def model_slug(model):
    return "".join(char if char.isalnum() else "_" for char in model).strip("_")


def parse_models(value):
    if value:
        return [model.strip() for model in value.split(",") if model.strip()]
    env_models = os.getenv("NVIDIA_NIM_MODELS") or os.getenv("NVIDIA_NIM_MODEL")
    if env_models:
        return [model.strip() for model in env_models.split(",") if model.strip()]
    return [
        "minimaxai/minimax-m2.7",
        "stepfun-ai/step-3.5-flash",
        "mistralai/mistral-large-3-675b-instruct-2512",
    ]


def dump_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False, sort_keys=True)


def load_env_file(start_path=None):
    start = Path(start_path or Path.cwd()).resolve()
    for directory in [start, *start.parents]:
        env_path = directory / ".env"
        if not env_path.exists():
            continue
        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)
        return env_path
    return None
