import dataclasses

from mitreattack.stix20 import MitreAttackData


class TechniquesRetriver:

    @staticmethod
    def get_object_by_techniques_id(object_stix_id: str, mitre_attack_data: MitreAttackData):
        list_objects = mitre_attack_data.get_campaigns_using_technique(object_stix_id)
        return list_objects

    @staticmethod
    def get_techniques_by_object_id():
        pass