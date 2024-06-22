import json
import yaml
import requests
import git

from os.path import exists

import yaml
from src.utils.FileUtils import save_to_json_file, read_from_json, extension_check  
from src.utils.Path import default_path, default_repo, CAPEC

def fetch_capec_data():
    """
    Metodo che permette di ottenere i dati dei CAPEC mediante request.
    """
        
    return __fetch_file(CAPEC,
                        "https://raw.githubusercontent.com/mitre/cti/master/capec/2.1/stix-capec.json", 'master')

def __fetch_file(domain: str, path_commit: str, branch: str):
    #filepath = f"{default_path}{domain}.json"
    file_json = None
    if not (__check_last_commit(domain, branch)): # and exists(filepath)):
        print("     ", domain, "change")
        if __check_internet_connection():
            
            # request
            file_text = requests.get(path_commit).text

            # modify extension
            if extension_check(path_commit, '.yaml'):
                file_json = yaml.safe_load(file_text)
            elif extension_check(path_commit, '.json'):
                file_json = json.loads(file_text)

            save_to_json_file(file_json, domain, default_path)

            # update and save data
            __update_local_hash(domain, __get_current_commit(domain, branch))
            return file_json
        
        else:
            raise ConnectionError("Internet connection is not available. Please connect to a network and try again!")
    else:
        print("     ", domain, "not change")

    # file already up-to-date
    
    return True


def __check_last_commit(domain: str, branch: str = 'master') -> bool:
    if __check_internet_connection():
        return __get_current_commit(domain, branch) == __get_last_local_hash(domain)
    else:
        return True


def __get_current_commit(domain: str, branch: str = 'master'):
    last_commit_sha = git.cmd.Git().ls_remote(default_repo, heads=True)
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