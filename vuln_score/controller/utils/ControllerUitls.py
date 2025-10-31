import re

cvwelibapi = "http://cvwelib/api/"


# Regex utils
__cve_regex = r"^(CVE-)\d{4}(-)\d{4,}$"
__cwe_regex = r"^(CWE-)\d*$"
__cvss_v31_regex = r"^(CVSS:([3][.][1])/AV:([N|A|L|P])/AC:([L|H])/PR:([N|L|H])/UI:([N|R])/S:([U|C])/C:([N|L|H])/I:([N|L|H])/A:([N|L|H]))$"

__invalid_cwe_ids = ['NVD-CWE-noinfo', 'NVD-CWE-Other']


def check_cve(cve_id: str) -> bool:
    return True if re.match(__cve_regex, cve_id) else False


def check_cwe(cwe_id: str) -> bool:
    return True if re.match(__cwe_regex, cwe_id) and cwe_id not in __invalid_cwe_ids else False


def check_cvss(vector_string: str) -> bool:
    return True if re.match(__cvss_v31_regex, vector_string) else False
