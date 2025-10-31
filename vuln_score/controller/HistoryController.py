import sys
sys.path.append('src')
import model.Dao as db
from datetime import datetime


def _get_history() -> list:
    return db.read_history()


def _add_history(new_history: dict) -> bool:
    most_recent = db.read_most_recent_history()
    new_id = __calculate_id(most_recent['id'] if 'id' in most_recent.keys() else None)
    
    # update new history field
    new_history['id'] = new_id
    new_history['date'] = datetime.now()
    return db.add_history(new_history)


def _search_history_id(keyword: str) -> list:
    out = []
    data = db.read_history()
    for run in data:
        if keyword in run['id']:
            out.append(run)
    return out


def __calculate_id(id: str):
    if id == None:
        return 'A-000'

    letter = id[0]
    num = int(id[2:])
    
    if num == 999:
        letter = chr(ord(letter)+1)
        num = 0
    else:
        num += 1

    return f'{letter}-{str(num).rjust(3, "0")}'
