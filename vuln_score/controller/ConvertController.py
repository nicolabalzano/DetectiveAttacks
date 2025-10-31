import sys
sys.path.append('src')
from controller.cvss.CVSSHelper import CVSSv31Tov4, _get_v31data_in_json

def _convert_cvss_to_v4(vector_string: str) -> dict:
    return CVSSv31Tov4(vector_string).get_json_data()


def _get_cvss_data(vector_string: str) -> dict:
    return _get_v31data_in_json(vector_string)
