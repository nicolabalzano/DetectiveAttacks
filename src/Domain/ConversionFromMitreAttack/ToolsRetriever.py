from pprint import pprint

from stix2.v20 import Tool

from src.Domain.ConversionFromMitreAttack.AbstractObjectWithAttackPatternRetriever import \
    AbstractObjectWithAttackPatternsRetriever
from src.Domain.ConversionFromMitreAttack.STIXBase20.ToolAndMalwareSTIX import ToolAndMalwareSTIX
from src.Domain.STIXObject.MyToolMalware import MyToolMalware
from src.Domain.Singleton import singleton
from src.Domain.MitreAttackData.MitreAttackData import mitre_attack_data

from stix2.v20 import Tool, Malware


@singleton
class ToolsRetriever(AbstractObjectWithAttackPatternsRetriever):
    _KEYS_TO_DELETE: tuple = (
        'x_mitre_modified_by_ref',
        'object_marking_refs',
        'x_mitre_aliases',
        'created_by_ref'
    )

    def __init__(self):
        super().__init__(MyToolMalware, ToolAndMalwareSTIX)

    def _get_all(self):
        return mitre_attack_data.get_software(remove_revoked_deprecated=True)

    def get_attack_patterns_relationship_using_objects_id(self, object_stix_id: str) -> tuple:
        return mitre_attack_data.get_techniques_used_by_software(object_stix_id)
