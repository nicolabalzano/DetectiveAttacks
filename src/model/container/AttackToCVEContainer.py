import nvdlib

from src.model.Singleton import singleton
from src.model.container.mySTIXContainer.AttackPatternsContainer import AttackPatternsContainer
from src.model.interfaceToMitre.conversionType.AttackToCVERetriever import AttackToCVERetriever
from src.model.interfaceToMitre.mitreData.mitreAttackToCVE.SentenceSimilarityModel import SentenceSimilarityModel


@singleton
class AttackToCVEContainer:
    i = 0
    MIN_SIMILARITY = 0.5

    def __init__(self, objects: dict):
        self.__objects = objects

    def reset_dataset(self, objects: dict):
        self.__objects = objects

    def get_data(self):
        return self.__objects

    def get_object_from_data_by_name(self, target_name: str):
        searched_obj = []
        for obj in self.__objects['mapping_objects']:
            if target_name.lower() in obj['capability_description'].lower():

                # if cve is not yet in the list
                searched_obj_in_list_searched = False
                for obj_in_searched_list in searched_obj:
                    if obj['capability_description'] == obj_in_searched_list['capability_description']:
                        searched_obj_in_list_searched = True

                if not searched_obj_in_list_searched:
                    searched_obj.append(obj)
        return searched_obj

    def get_objects_from_data_by_cve_id(self, target_id: str):
        searched_obj = []
        for obj in self.__objects['mapping_objects']:
            if target_id.lower() in obj['capability_id'].lower():
                searched_obj.append(obj)
                """
                # if cve is not yet in the list
                searched_obj_in_list_searched = False
                for obj_in_searched_list in searched_obj:
                    if obj['capability_id'] == obj_in_searched_list['capability_id']:
                        searched_obj_in_list_searched = True

                if not searched_obj_in_list_searched:
                    searched_obj.append(obj)
                    """
        return searched_obj

    def get_object_from_data_by_cve_id(self, target_id: str):
        searched_obj = []
        for obj in self.__objects['mapping_objects']:
            if target_id.lower() in obj['capability_id'].lower():

                # if cve is not yet in the list
                searched_obj_in_list_searched = False
                for obj_in_searched_list in searched_obj:
                    if obj['capability_id'] == obj_in_searched_list['capability_id']:
                        searched_obj_in_list_searched = True

                if not searched_obj_in_list_searched:
                    searched_obj.append(obj)

        return searched_obj

    def __get_attack_pattern_by_cve_id_in_mapped(self, target_id: str):
        dict_at_type_rel = {}

        # index to get previous CVE ID to stop the iteration
        for index, obj in enumerate(self.__objects['mapping_objects']):
            # if the cve is found
            if obj["capability_id"] == target_id and obj['status'] == 'complete':
                at = AttackPatternsContainer().get_object_from_data_by_mitre_id(obj['attack_object_id'].strip())

                if obj["mapping_type"] not in dict_at_type_rel:
                    # if there is key
                    dict_at_type_rel[obj["mapping_type"]] = [at]
                else:
                    # if there isn't key, add to the list
                    dict_at_type_rel[obj["mapping_type"]].append(at)

        return dict_at_type_rel

    def get_attack_pattern_by_cve_id(self, target_id: str) -> dict:
        dict_result = self.__get_attack_pattern_by_cve_id_in_mapped(target_id)

        # if the cve is not mapped
        if not dict_result:
            cve = nvdlib.searchCVE(cveId=target_id)[0]

            at_related = []

            # if CVE isn't map in MITRE ENGENUITY use SMET to determinate
            if not dict_result:
                # if cosine similarity is >= 0.5 add attack to related list of attacks
                """
                at_related = [at for at in AttackPatternsContainer().get_data() if
                              AttackBert().check_similarity(cve.descriptions[0].value, at.description) >= MIN_SIMILARITY]
                """
                for at in AttackPatternsContainer().get_data():
                    self.i += 1
                    print(self.i)
                    sim = SentenceSimilarityModel().check_similarity(cve.descriptions[0].value, at.description)
                    if sim >= self.MIN_SIMILARITY:
                        print(at.name, sim)
                        at_related.append(at)

                self.i = 0
                dict_result = {'uncategorized': at_related}

                # save new mapping for future research
                SentenceSimilarityModel().save_new_mapping(cve, at_related)

                # update the dataset with new mapping
                self.reset_dataset(AttackToCVERetriever().get_all_objects())

        return dict_result

    def get_cve_id_by_attack_pattern_mitre_id(self, attack_pattern_mitre_id: str) -> list[dict]:
        """
        This method get the CVE releated of an attack pattern

        Parameters
        ----------
        attack_pattern_mitre_id : str
            the MITRE ID of the attack pattern

        Returns
        -------
            a list of  {"type of relationship" (ex. primary_impact, secondary_impact, exploitation_technique, uncategorized): cve_id }
        """
        list_cve_id = []

        for obj in self.__objects['mapping_objects']:
            dict_cve_id = {}

            # if attack id is found
            if attack_pattern_mitre_id == obj['attack_object_id'] and obj['status'] == 'complete':
                dict_cve_id[obj["capability_id"]] = [obj["mapping_type"]]

            # if dict is not empty
            if dict_cve_id:
                list_cve_id.append(dict_cve_id)

        return list_cve_id
