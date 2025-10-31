import sys
sys.path.append('src')
from controller.cve.CVEHelper import CVE
from controller.utils.ControllerUitls import check_cwe
import controller.cve.ScoreHelper as sh
import controller.SearchController as sc
import requests

__detective_attacks = "http://10.11.97.30:8080/api/stix_and_vulnerability/get_data/get_related_cves_and_assets_of_cve"


def _new_research(cve_id: str) -> dict:
    cve_list = __get_all_relationships(cve_id)
    detailed_cve_list = []
    for cve in cve_list.keys():
        data = sc._get_cve_from_id(cve)
        if data != {}:
            data['assetIds'] = cve_list[data['id']]
            detailed_cve_list.append(CVE(data))
    severity_counts = __get_severity_counts(detailed_cve_list)
    weakness_counts = __get_weakness_counts(detailed_cve_list)
    # base_score = sh.calculate_org_score_based_on_exploitability(detailed_cve_list)
    base_score = sh.calculate_org_score_based_on_exploitability(detailed_cve_list)
    return {
        "criticalVuln": severity_counts['CRITICAL'],
        "highVuln": severity_counts['HIGH'],
        "mediumVuln": severity_counts['MEDIUM'],
        "lowVuln": severity_counts['LOW'],
        "primaryWeak": weakness_counts['Primary'],
        "secondaryWeak": weakness_counts['Secondary'],
        "score": base_score,
        "state": sh.compute_estimated_severity(base_score),
        "cveList": [__tinify_json(cve.cve_json, cve_list[cve.cve_id]) for cve in detailed_cve_list],
        "cveCount": len(cve_list),
        "cweCount": weakness_counts['Primary'] + weakness_counts['Secondary']
    }


def __tinify_json(orignal: dict, assets: list) -> dict:
    out = orignal
    out.pop('configurations', None)
    out.pop('references', None)
    return out


def __get_all_relationships(cve_id: str) -> dict:
    # TO-DO: request to third-party API
    """
    cve_list = {
        'CVE-2014-3757':['A0008', 'A0012'],
        'CVE-2018-16659':['A0012'],
        'CVE-2018-2925':['A0006'],
        'CVE-2006-3414':['A0008'],
        'CVE-2021-30303':['A0005', 'A0011'],
        'CVE-2010-3686':['A0012'],
        'CVE-2020-23912':['A0008', 'A0014'],
        'CVE-2024-0007':['A0007', 'A0012'],
        'CVE-2024-1011':['A0008', 'A0012'],
        'CVE-2012-1297':['A0008'],
        'CVE-2012-1947':[],
        'CVE-2008-1515':[],
        'CVE-2017-15425':['A0008', 'A0012'],
        'CVE-2017-18158':[],
        'CVE-2010-3685':['A0008', 'A0012']
    }
    """
    cve_list = requests.get(f"{__detective_attacks}?id={cve_id}")
    return cve_list


def __get_severity_counts(cve_list: list[CVE]) -> dict:
    out = {
        "CRITICAL": 0,
        "HIGH": 0,
        "MEDIUM": 0,
        "LOW": 0,
        "NONE": 0
    }
    for cve in cve_list:
        out[cve.get_cvss_severity()] += 1
    return out


def __get_weakness_counts(cve_list: list[CVE]) -> dict:
    added_cwes = []
    out = {
        'Primary': 0,
        'Secondary': 0
    }
    for cve in cve_list:
        for cwe in cve.get_cwes():
            if cwe[0] not in added_cwes and check_cwe(cwe[0]):
                out[cwe[1]] += 1
                added_cwes.append(cwe[0])
    return out
