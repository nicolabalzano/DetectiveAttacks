import json
import os


class MitreAttackToCVEData:

    def __init__(self, filepath: str = None):
        if os.path.isfile(filepath):
            with open(filepath, 'r') as file:
                self.dict_file = json.load(file)

    def get_all(self):
        return self.dict_file
