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

    def get_attack_pattern_by_cve_id(self, target_id: str) -> list:
        for obj in self.__objects:
            if obj["CVE ID"] == target_id:
                return obj

        # if CVE isn't map in MITRE ENGENUITY use SMET to determinate
        cve = nvdlib.searchCVE(cveId=target_id)[0]

        # if cosine similarity is > 0.5 add attack to related list of attacks
        at_related = [at for at in AttackPatternsContainer().get_data() if
                      AttackBert().check_similarity(cve.descriptions[0].value, at.description) > 0.5]

        return at_related

    def get_cve_id_by_attack_pattern_mitre_id(self, attack_pattern_mitre_id: str) -> list:
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

        for obj in self.__objects:
            dict_cve_id = {}

            if attack_pattern_mitre_id in obj['Primary Impact']:
                dict_cve_id['Primary Impact'] = obj["CVE ID"]
            if attack_pattern_mitre_id in obj['Secondary Impact']:
                dict_cve_id['Secondary Impact'] = obj["CVE ID"]
            if attack_pattern_mitre_id in obj['Exploitation Technique']:
                dict_cve_id['Exploitation Technique'] = obj["CVE ID"]
            if attack_pattern_mitre_id in obj['Uncategorized']:
                dict_cve_id['Uncategorized'] = obj["CVE ID"]

            # fi dict is not empty
            if dict_cve_id:
                list_cve_id.append(dict_cve_id)

        return list_cve_id
