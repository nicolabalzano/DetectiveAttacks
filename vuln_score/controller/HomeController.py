import sys
sys.path.append('src')
from controller.utils.ControllerUitls import cvwelibapi
import requests
import json


def _get_cwe_count() -> dict:
    result = requests.get(f"{cvwelibapi}get_cwe?cweCount")
    return json.loads(result.content)


def _get_cve_count() -> dict:
    result = requests.get(f"{cvwelibapi}get_cve?cveCount")
    return json.loads(result.content)
