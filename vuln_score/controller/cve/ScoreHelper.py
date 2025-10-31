import sys
sys.path.append('src')
import numpy as np
import model.Dao as db
from typing import List
from controller.cve.CVEHelper import CVE
from controller.cvss.CVSSHelper import CVSSv31Tov4

severity_score_mapping = {
    "NONE": 0,
    "LOW": 1,
    "MEDIUM": 2,
    "HIGH": 3,
    "CRITICAL": 4
}

cwe_type_mapping = {
    "PRIMARY": 2,
    "SECONDARY": 1,
}

__exploitability_score_max_v2 = 10.0  # obtained from: 20.0 x AV x AC x A for v2.0
__exploitability_score_max_v3 = 3.90  # obtained from: 8.22 x AV x AC x PR x UI for v3.1

__severity_score_max = 4.0  # obtained from severity_score_mapping max value

__impact_based_max_v2 = 10.0  # obtained from: 10.41 x [ 1 - (1 - Confidentiality) x (1 - Integrity) x (1 - Availability) ]
__impact_based_max_v3 = 6.0  # obtained from: 7.52 × (ISS - 0.029) - 3.25 × (ISS - 0.02)^15 where ISS = 1 - [ (1 - Confidentiality) × (1 - Integrity) × (1 - Availability) ]

__asset_based_max = 10.0 # obtained arbitrarily


def calculate_base_org_score(cve_list: List[CVE]) -> float:
    """
    Description:
        Calculates the final organisation score based on the following criteria:\n
        The score is the simple average of all the CVE base scores.\n
        This approach does not take into account the impact/weigh of every vulnerability found, but gives a simple,
        straight-forward perspective of the overall security score
    :param cve_list: List of all the detected CVEs
    :return: Final organisation score
    """
    score = sum(cve.get_cvss_base_score() for cve in cve_list) / len(cve_list)
    return round(score, 2)


def calculate_base_org_score_v4(cve_list: List[CVSSv31Tov4]) -> float:
    """
    Description:
        Calculates the final organisation score based on the following criteria:\n
        The score is the simple average of all the CVE 4.0 base scores.\n
        This approach does not take into account the impact/weigh of every vulnerability found, but gives a simple,
        straight-forward perspective of the overall security score
    :param cve_list: List of all the detected CVEs
    :return: Final organisation score
    """
    score = sum(cve.estimated_base_score for cve in cve_list) / len(cve_list)
    return round(score, 2)


def calculate_org_score_based_on_exploitability(cve_list: List[CVE]) -> float:
    """
    Description:
        Calculates the final organisation score based on the following criteria:\n
        The score is the weighted average of all the CVE base scores multiplied by their respective exploitability score.\n
        The exploitability score, which indicates the likelihood of that vulnerability to be exploited and/or the ease of
        exploitation can be a good mean of measure to weigh every CVE and obtain a nicely, informative weighted result
    :param cve_list: List of all the detected CVEs
    :return: Final organisation score
    """
    # for each cve we separate v2s from v3s
    v2cves = []
    v3cves = []
    for cve in cve_list:
        vers = cve.get_cvss_version()
        if vers == '2.0':
            v2cves.append(cve)
        elif vers in ['3.0', '3.1']:
            v3cves.append(cve)

    datav2 = np.array([(cve.get_cvss_base_score() * cve.get_exploitability_score()) for cve in v2cves])
    datav3 = np.array([(cve.get_cvss_base_score() * cve.get_exploitability_score()) for cve in v3cves])
    scorev2 = (sum(__normalize_score(datav2, __exploitability_score_max_v2)) / len(datav2)) if len(datav2) != 0 else None
    scorev3 = (sum(__normalize_score(datav3, __exploitability_score_max_v3)) / len(datav3)) if len(datav3) != 0 else None

    # calculate final score
    if scorev2 == None and scorev3 == None:
        return round(0, 2)

    score = None
    if scorev2 == None:
        score = scorev3
    elif scorev3 == None:
        score = scorev2
    else:
        score = (scorev2 + scorev3) / 2

    return round(score, 2)


def calculate_org_score_based_on_severity(cve_list: List[CVE]) -> float:
    """
    Description:
        Calculates the final organisation score based on the following criteria:\n
        The score is the weighted average of all the CVE base scores multiplied by their respective severity score,
        mapped as follows:
            - "NONE" = 0
            - "LOW" = 1
            - "MEDIUM" = 2
            - "HIGH" = 3
            - "CRITICAL" = 4
        The severity score, which indicates the underlying CVSS score in a string format, can be a good mean of measure
        to weigh every CVE and obtain a nicely, informative weighted result
    :param cve_list: List of all the detected CVEs
    :return: Final organisation score
    """
    # for each cve in the list we add the base score value weighted on its severity score mapping
    data = np.array([(cve.get_cvss_base_score() * severity_score_mapping[cve.get_cvss_severity().upper()]) for cve in
                     cve_list])
    score = sum(__normalize_score(data, __severity_score_max)) / len(cve_list)
    return round(score, 2)


def calculate_org_score_based_on_severity_v4(cve_list: List[CVSSv31Tov4]) -> float:
    """
    Description:
        Calculates the final organisation score based on the following criteria:\n
        The score is the weighted average of all the CVE 4.0 base scores multiplied by their respective severity score,
        mapped as follows:
            - "NONE" = 0
            - "LOW" = 1
            - "MEDIUM" = 2
            - "HIGH" = 3
            - "CRITICAL" = 4
        The severity score, which indicates the underlying CVSS score in a string format, can be a good mean of measure
        to weigh every CVE and obtain a nicely, informative weighted result
    :param cve_list: List of all the detected CVEs
    :return: Final organisation score
    """
    # for each cve in the list we add the base score value weighted on its severity score mapping
    data = np.array([(cve.estimated_base_score * severity_score_mapping[cve.estimated_severity.upper()]) for cve in
                     cve_list])
    score = sum(__normalize_score(data, __severity_score_max)) / len(cve_list)
    return round(score, 2)


def calculate_org_score_based_on_impact_score(cve_list: List[CVE]) -> float:
    """
    Description:
        Calculates the final organisation score based on the following criteria:\n
        The score is the weighted average of all the CVE base scores multiplied by their respective impact score.\n
        The impact score, which indicates, as the name suggests, the impact of a vulnerability on the company's Risk
        index, can be a good mean of measure to weigh every CVE and obtain a nicely, informative weighted result
    :param cve_list: List of all the detected CVEs
    :return: Final organisation score
    """
    # for each cve we separate v2s from v3s
    v2cves = []
    v3cves = []
    for cve in cve_list:
        vers = cve.get_cvss_version()
        if vers == '2.0':
            v2cves.append(cve)
        elif vers in ['3.0', '3.1']:
            v3cves.append(cve)

    datav2 = np.array([(cve.get_cvss_base_score() * cve.get_impact_score()) for cve in v2cves])
    datav3 = np.array([(cve.get_cvss_base_score() * cve.get_impact_score()) for cve in v3cves])
    scorev2 = (sum(__normalize_score(datav2, __impact_based_max_v2)) / len(datav2)) if len(datav2) != 0 else None
    scorev3 = (sum(__normalize_score(datav3, __impact_based_max_v3)) / len(datav3)) if len(datav3) != 0 else None

    # calculate final score
    if scorev2 == None and scorev3 == None:
        return round(0, 2)

    score = None
    if scorev2 == None:
        score = scorev3
    elif scorev3 == None:
        score = scorev2
    else:
        score = (scorev2 + scorev3) / 2

    return round(score, 2)


def calculate_org_score_based_on_cwes(cve_list: List[CVE], mode: str = 'count') -> float:
    """
    Description:
        Calculates the final organisation score based on the following mode criterias:\n
        Mode:
            - count: Calculates the score as the weighted average of all the CVE base scores multiplied by the number of weaknesses linked to the specific CVE
            - type: Calculates the score as the weighted average of all the CVE base scores multiplied by the 'type' of weaknesses linked to the specific CVE, mapped on an internal dictionary
            - both: Calculates the score as the average of the previous mentioned modes
    :param cve_list: List of all the detected CVEs
    :param mode: Calculation mode between count | type | both (default = count)
    :return: Final organisation score based on the chosen mode
    :raises ValueError: if the inserted mode is not valid
    """
    if mode not in ['count', 'type', 'both']:
        raise ValueError("Inserted mode not valid, please choose between 'count', 'type' or 'both'")

    # process CWE score based on mode
    if mode == 'count':
        score = __score_based_on_cwe_count(cve_list)
    elif mode == 'type':
        score = __score_based_on_cwe_type(cve_list)
    else:
        score = (__score_based_on_cwe_count(cve_list) + __score_based_on_cwe_type(cve_list)) / 2
    return round(score, 2)


def calculate_org_score_based_on_assets(cve_list: List[CVE]):
    """
    Description:
        Calculates the final organisation score based on the following criteria:\n
        The score is the weighted average of all the base scores multiplied by their respective asset weights (declared by the user).
        The assets may, or many not, be related to all or none of the previously mentioned CVEs. The final score takes into consideration
        only the vulnerabilities which include asset identifiers. Those not matching such criteria are excluded from the final score, therefore
        it might result into a relatively low-reliability score indication.
    :param cve_list: List of all the detected CVEs
    :return: Final organisation score
    """
    # for each cve in the list we add the base score value weighted on its respective assets values score mapping
    data = np.array([])
    skipped_vulns = 0

    for cve in cve_list:
        if len(cve.assetIds) == 0:
            skipped_vulns += 1
            continue
        partial = np.array([(cve.get_cvss_base_score() * db.get_asset_weight(asset_id)) for asset_id in cve.assetIds])
        data = np.append(data, sum(__normalize_score(partial, __asset_based_max))/len(cve.assetIds))

    score = (sum(data) / (len(cve_list) - skipped_vulns)) if len(cve_list) - skipped_vulns != 0 else 0
    return round(score, 2)


def compute_estimated_severity(base_score: float) -> str:
    if base_score == 0.0:
        return "NONE"
    elif base_score <= 3.9:
        return "LOW"
    elif base_score <= 6.9:
        return "MEDIUM"
    elif base_score <= 8.9:
        return "HIGH"
    else:
        return "CRITICAL"


def __score_based_on_cwe_count(cve_list: List[CVE]) -> float:
    """
    Calculates the score as the weighted average of all the CVE base scores multiplied by the count of weaknesses
    linked to the CVE
    :param cve_list: List of all the detected CVEs
    :return: Score
    """
    data = np.array([(cve.get_cvss_base_score() * len(cve.get_cwes())) for cve in cve_list])
    return sum(__normalize_cwe_score(data)) / len(cve_list)


def __score_based_on_cwe_type(cve_list: List[CVE]) -> float:
    """
    Calculates the score as the weighted average of all the CVE base scores multiplied by the average of all the
    mapped weaknesses types on an internal dictionary
    :param cve_list: List of all the detected CVEs
    :return: Score
    """
    data = np.fromiter((cve.get_cvss_base_score() * (sum(cwe_type_mapping[t[1].upper()] for t in cve.get_cwes()) / len(cve.get_cwes())) for cve in cve_list), float)
    return sum(__normalize_cwe_score(data)) / len(cve_list)


def __normalize_score(data, norm_max: float, norm_min: float = 0.0):
    if (norm_max - norm_min) == 0:
        raise ZeroDivisionError
    return (data - norm_min) / (norm_max - norm_min)


def __normalize_cwe_score(data):
    if len(data) == 1:
        return data
    if (np.max(data) - np.min(data)) == 0:
        raise ZeroDivisionError
    return ((data - np.min(data)) / (np.max(data) - np.min(data))) * 10.0
