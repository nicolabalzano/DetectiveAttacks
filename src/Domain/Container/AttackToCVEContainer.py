import nvdlib

from src.domain.Singleton import singleton
from src.domain.container.AttackPatternsContainer import AttackPatternsContainer
from src.domain.interfaceToMitre.mitreData.mitreAttackToCVE.AttackBert import AttackBert


@singleton
class AttackToCVEContainer:

    def __init__(self, objects: dict):
        self.__objects = objects

    def get_data(self):
        return self.__objects

    def __get_attack_pattern_by_cve_id_in_mapped(self, target_id: str):
        dict_at_type_rel = {}

        # index to get previous CVE ID to stop the iteration
        for index, obj in enumerate(self.__objects['mapping_objects']):
            # if the cve is found
            if obj["capability_id"] == target_id and obj['status'] == 'complete':
                if obj["mapping_type"] not in dict_at_type_rel:
                    # if there is key
                    dict_at_type_rel[obj["mapping_type"]] = [
                        AttackPatternsContainer().get_object_from_data_by_mitre_id(obj['attack_object_id'])]
                else:
                    # if there isn't key, add to the list
                    dict_at_type_rel[obj["mapping_type"]].append(
                        AttackPatternsContainer().get_object_from_data_by_mitre_id(obj['attack_object_id']))

        return dict_at_type_rel

    def get_attack_pattern_by_cve_id(self, target_id: str) -> dict:
        dict_result = self.__get_attack_pattern_by_cve_id_in_mapped(target_id)

        if not dict_result:
            # if CVE isn't map in MITRE ENGENUITY use SMET to determinate
            cve = nvdlib.searchCVE(cveId=target_id)[0]

            # if cosine similarity is > 0.5 add attack to related list of attacks
            at_related = [at for at in AttackPatternsContainer().get_data() if
                          AttackBert().check_similarity(cve.descriptions[0].value, at.description) > 0.5]

            dict_result = {'uncategorized': at_related}

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

                if obj["mapping_type"] not in dict_cve_id:
                    # if there is key
                    dict_cve_id[obj["mapping_type"]] = [obj["capability_id"]]
                else:
                    # if there isn't key, add to the list
                    dict_cve_id[obj["mapping_type"]].append(obj["capability_id"])

            # if dict is not empty
            if dict_cve_id:
                list_cve_id.append(dict_cve_id)

        return list_cve_id
