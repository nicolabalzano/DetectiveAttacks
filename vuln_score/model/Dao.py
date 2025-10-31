import sys
sys.path.append('src')
from utils.ToFileUtils import get_json_from_file, save_to_json_file
import time

# History
__DEFAULT_PATH = 'src/model/files/'
__HISTORY_DATA = 'HISTORY.json'
__ASSETS_DATA = 'ASSETS.json'


def read_assets() -> list:
    return __get_file(__ASSETS_DATA)


def update_asset_score(asset_id: str, score: float) -> bool:
    data = __get_file(__ASSETS_DATA)
    for asset in data:
        if asset['id'] == asset_id:
            asset['score'] = score
            save_to_json_file(data,__ASSETS_DATA, __DEFAULT_PATH)
            return True
    return False


def get_asset_weight(asset_id: str) -> float:
    data = __get_file(__ASSETS_DATA)
    for asset in data:
        if asset['id'] == asset_id:
            return asset['score']


def read_history(order: int = 1) -> list:
    """
        Desc:
            Retrieves the saved HISTORY DATA file. If no file is found,
            it creates a new empty list
        Params:
            order: 0 - ascending, 1 - descending
        Returns:
            A list containing all the fetched history data
    """
    data  = __get_file(__HISTORY_DATA)
    match order:
        case 0:
            # ascending - do nothing
            if len(data) > 0 and data != []:
                return sorted(data, key=__sort_by_date)
        case 1:
            # descending
            if len(data) > 0 and data != []:
                return list(reversed(sorted(data, key=__sort_by_date)))
        case _:
            raise ValueError('Invalid requested order')


def __get_file(filename: str) -> list:
    data = []
    try:
        data = get_json_from_file(filename, __DEFAULT_PATH)
    except:
        save_to_json_file([], filename, __DEFAULT_PATH)
    return data


def read_most_recent_history() -> dict:
    """
        Desc:
            Retrieves the most recent history saved
        Returns:
            A dict representing the most recent history element
    """
    curr_data = __get_file(__HISTORY_DATA)
    if len(curr_data) > 0 and curr_data != []:
        curr_data.sort(key=__sort_by_date)
        return curr_data[-1]
    return {}


def add_history(new_history: dict) -> bool:
    """
        Desc:
            Adds a new History field to the default HISTORY_DATA file
        Params:
            :param new_history: The new history dict
        Returns:
            True if the file is saved successfully, else False
    """
    try:
        curr_data = __get_file(__HISTORY_DATA)
        curr_data.append(new_history)
        save_to_json_file(curr_data, __HISTORY_DATA, __DEFAULT_PATH)
    except FileNotFoundError:
        return False
    return True


def __sort_by_date(e):
    return time.mktime(time.strptime(e['date'], '%Y-%m-%d %H:%M:%S.%f'))
