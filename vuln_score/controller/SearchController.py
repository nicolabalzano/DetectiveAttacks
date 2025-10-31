import sys
sys.path.append('src')
from controller.utils.ControllerUitls import cvwelibapi
import requests
import json


def _get_cve_from_id(cve_id: str) -> dict:
    result = requests.get(f"{cvwelibapi}get_cve?cveId={cve_id}")
    return json.loads(result.content)
