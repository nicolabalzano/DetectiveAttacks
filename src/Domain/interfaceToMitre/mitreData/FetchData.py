import json

import requests
import git

from os.path import exists

import yaml

from src.domain.interfaceToMitre.mitreData.utils.Path import ENTERPRISE_ATTACK, \
    MOBILE_ATTACK, ICS_ATTACK, ATLAS, default_path, default_repos, ATTACK_TO_CVE
from src.domain.interfaceToMitre.mitreData.utils.FileUtils import save_to_json_file, read_from_json, \
    extension_check, conversion_csv_string_to_json_string


def fetch_enterprise_data() -> bool:
    """
    Metodo che permette di ottenere i dati dell'ATT&CK ENTERPRISE STIX dal MITRE/CTI mediante request.
    """
    return __fetch_file(ENTERPRISE_ATTACK,
                        f"https://raw.githubusercontent.com/mitre/cti/master/{ENTERPRISE_ATTACK}/{ENTERPRISE_ATTACK}.json",
                        'master')


def fetch_mobile_data() -> bool:
    """
    Metodo che permette di ottenere i dati dell'ATT&CK MOBILE STIX dal MITRE/CTI mediante request.
    """

    return __fetch_file(MOBILE_ATTACK,
                        f"https://raw.githubusercontent.com/mitre/cti/master/{MOBILE_ATTACK}/{MOBILE_ATTACK}.json",
                        'master')


def fetch_ics_data() -> bool:
    """
    Metodo che permette di ottenere i dati dell'ATT&CK ICS STIX dal MITRE/CTI mediante request.
    """
    return __fetch_file(ICS_ATTACK,
                        f"https://raw.githubusercontent.com/mitre/cti/master/{ICS_ATTACK}/{ICS_ATTACK}.json", 'master')


def fetch_atlas_data() -> bool:
    """
    Metodo che permette di ottenere i dati dell'ATLAS mediante request.
    """
    return __fetch_file(ATLAS,
                        "https://raw.githubusercontent.com/mitre-atlas/atlas-data/main/dist/ATLAS.yaml", 'main')


def fetch_attack_to_cve_data():
    """
        Metodo che permette di ottenere la mappatura CVE ATTACK mediante request.
        """
    return __fetch_file(ATTACK_TO_CVE,
                        'https://raw.githubusercontent.com/center-for-threat-informed-defense/attack_to_cve/master/Att%26ckToCveMappings.csv', 'master')


def __fetch_file(domain: str, path: str, branch: str):
    filepath = f"{default_path}{domain}.json"
    file_json = None
    if not (__check_last_commit(domain) and exists(filepath)):
        if __check_internet_connection():
            # request
            file_text = requests.get(path).text

            # modify extension
            if extension_check(path, '.yaml'):
                file_json = yaml.safe_load(file_text)
            elif extension_check(path, '.json'):
                file_json = json.loads(file_text)
            elif extension_check(path, '.csv'):
                file_json = json.loads(conversion_csv_string_to_json_string(file_text))

            # update and save data
            __update_local_hash(domain, __get_current_commit(domain, branch))
            save_to_json_file(file_json, domain, default_path)
            return file_json
        else:
            raise ConnectionError("Internet connection is not available. Please connect to a network and try again!")

    # file already up-to-date
    return True


def __check_last_commit(domain: str, branch: str = 'master') -> bool:
    return __get_current_commit(domain, branch) == __get_last_local_hash(domain)


def __get_current_commit(domain: str, branch: str = 'master'):
    last_commit_sha = git.cmd.Git().ls_remote(default_repos[domain], heads=True)
    for string in str(last_commit_sha).split("\n"):
        if string.__contains__(branch):
            return string[0:40]


def __get_last_local_hash(domain: str) -> str:
    return read_from_json(default_path, "local-hashes")[domain]


def __update_local_hash(domain: str, new_hash: str):
    data = read_from_json(default_path, "local-hashes")
    data[domain] = new_hash
    save_to_json_file(data, "local-hashes", f"{default_path}")


def __check_internet_connection() -> bool:
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False
