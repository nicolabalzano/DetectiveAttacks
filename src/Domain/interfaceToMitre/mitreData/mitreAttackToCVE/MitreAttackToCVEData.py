import json
import os


class MitreAttackToCVEData:

    def __init__(self, filepath: str = None, filepath_bert_history: str = None):

        if os.path.isfile(filepath):
            with open(filepath, 'r') as file:
                dict_file = json.load(file)

            # if there is a bert history
            if os.path.isfile(filepath_bert_history):
                with open(filepath_bert_history, 'r') as file_bert_history:
                    dict_file_bert_history = json.load(file_bert_history)

                # for duplicate key mapping_objects, union the lists
                self.dict_file = {**dict_file_bert_history, **dict_file,
                                  'mapping_objects': dict_file['mapping_objects'] + dict_file_bert_history['mapping_objects']}

            # if there isn't bert history
            else:
                self.dict_file = dict_file

    def get_all(self):
        return self.dict_file
