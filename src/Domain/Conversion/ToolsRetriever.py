from pprint import pprint

from stix2.v20 import Tool

from src.Domain.Conversion.AbstractObjectWithTechniquesRetriever import AbstractObjectWithTechniquesRetriever
from src.Domain.STIXObject.MyTool import MyTool
from src.Domain.Singleton import singleton
from src.Domain.MitreAttackData.MitreAttackData import mitre_attack_data


@singleton
class ToolsRetriever(AbstractObjectWithTechniquesRetriever):

    _KEYS_TO_DELETE: tuple = (
        'x_mitre_modified_by_ref',
        'object_marking_refs',
        'x_mitre_aliases',
        'created_by_ref'
    )

    def __init__(self):
        super().__init__(MyTool, Tool)

    def _get_all(self):
        return mitre_attack_data.get_software(remove_revoked_deprecated=True)

    def get_objects_using_technique_id(self, object_stix_id: str):
        return mitre_attack_data.get_software_using_technique(object_stix_id)