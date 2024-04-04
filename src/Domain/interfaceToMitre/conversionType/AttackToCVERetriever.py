from src.domain.Singleton import singleton
from src.domain.interfaceToMitre.mitreData.MitreData import MITRE_ATTACK_TO_CVE


@singleton
class AttackToCVERetriever:

    def get_all_objects(self) -> dict:
        dict_cve_attacks = MITRE_ATTACK_TO_CVE.get_all()
        return dict_cve_attacks

