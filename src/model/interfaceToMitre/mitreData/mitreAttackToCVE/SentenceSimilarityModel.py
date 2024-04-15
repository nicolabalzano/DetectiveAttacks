import traceback

import nvdlib
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from src.model.Singleton import singleton
from src.model.interfaceToMitre.mitreData.utils.FileUtils import check_exist_file_json, save_to_json_file, \
    read_from_json
from src.model.interfaceToMitre.mitreData.utils.Path import default_path, ATTACK_TO_CVE_SSM_HISTORY


@singleton
class SentenceSimilarityModel:

    def __init__(self):
        # BlueAvenir/sti_cyber_security_model_V_0_1
        # basel/ATTACK-BERT
        self.model = SentenceTransformer('BlueAvenir/sti_cyber_security_model_V_0_1')

    def check_similarity(self, sentence1: str, sentence2: str):
        embeddings = self.model.encode([sentence1, sentence2])
        cosine_similarity_number = cosine_similarity([embeddings[0]], [embeddings[1]])
        return cosine_similarity_number[0][0]

    @staticmethod
    def save_new_mapping(cve, list_of_attack_patterns: list):

        # check if file exist
        if not check_exist_file_json(ATTACK_TO_CVE_SSM_HISTORY, default_path):
            save_to_json_file({'mapping_objects': []}, ATTACK_TO_CVE_SSM_HISTORY, default_path)

        dict_bert_history = read_from_json(default_path, ATTACK_TO_CVE_SSM_HISTORY)

        for at in list_of_attack_patterns:
            dict_mapping = {
                "comments": "",
                "attack_object_id": at.x_mitre_id,
                "attack_object_name": at.name,
                "references": [],
                "capability_description": cve.descriptions[0].value.split('.')[0],
                "capability_id": cve.id,
                "mapping_type": "uncategorized",
                "capability_group": cve.id.split('-')[1],
                "status": "complete"
            }

            dict_bert_history["mapping_objects"].append(dict_mapping)

        # save new mapping
        save_to_json_file(dict_bert_history, ATTACK_TO_CVE_SSM_HISTORY, default_path)
